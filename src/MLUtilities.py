import numpy as np
import tensorflow as tf


# Here the Baseline class inherits
# from the tf.keras.Model
class Baseline(tf.keras.Model):
    
    """ Baseline model for comparison """
    
    def __init__(self, label_index=None):
        super().__init__()
        self.label_index = label_index

    def call(self, inputs):
        if self.label_index is None:
            return inputs
        result = inputs[:, :, self.label_index]
        return result[:, :, tf.newaxis]

    

# Residual wrapper

class ResidualWrapper(tf.keras.Model):
    
    """Residual wrapper class """
    
    def __init__(self, model):
        super().__init__()
        self.model = model

    def call(self, inputs, *args, **kwargs):
        delta = self.model(inputs, *args, **kwargs)

        # The prediction for each time step is the input
        # from the previous time step plus the delta
        # calculated by the model.
        return inputs + delta
    


# Training driver
def compile_and_fit(model, window, patience=2,
                    tbCallback=None, MAX_EPOCHS=100):
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

    model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError()])

    history = model.fit(window.train, epochs=MAX_EPOCHS,
                      validation_data=window.val,
                      callbacks=[early_stopping,tbCallback])
    return history