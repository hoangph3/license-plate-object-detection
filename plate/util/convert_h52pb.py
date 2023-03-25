import tensorflow as tf
from tensorflow.contrib.keras import backend as K
from util import load_model


K.set_learning_phase(0)
model_path = "../serving/wpod-net.json"
model = load_model(model_path)

export_path = '../serving/1'
with K.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input': model.input},
        outputs={'output': model.output}
    )
    print('Converted to SavedModel!!!')
