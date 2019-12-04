from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop


batch_size = 128
num_classes = 10
epochs = 1

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(784,)))
model.add(Dense(32, activation='relu', input_shape=(128,)))
model.add(Dense(num_classes, activation='relu'))


model.summary()

model.compile(loss='mean_squared_error',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)


###############

src = open("cpu_0.h", "w");
print("#define RUN_LAYERS \\", file=src);
layer_id = 0;
for layer in model.layers:
    layer_id=layer_id+1;
    if (layer_id == len(model.layers)):
        print("process"+str(layer_id)+"();", file=src);
    else:
        print("process"+str(layer_id)+"(); \\", file=src);        
src.close();


layer_id = 0;
for layer in model.layers:
    layer_id=layer_id+1;
    print("Layer:", layer);
    src = open("cpu_"+str(layer_id)+".h", "w");
    print("extern REAL max(REAL,REAL);",file=src);
    weights = layer.get_weights();
    
    # Create the buffer
    print ("extern struct { REAL val[",len(weights[0]),"]; } frame_"+str(layer_id)+";",file=src);
    if (layer_id == len(model.layers)):
        print ("extern struct { REAL val[",len(weights[0][0]),"]; } final_frame;",file=src);
    else:
        print ("struct { REAL val[",len(weights[0][0]),"]; } frame_"+str(layer_id+1)+";",file=src);
    
    print("#define WEIGHT w_"+str(layer_id), file=src);
    print("#define BIAS b_"+str(layer_id), file=src);
    print("#define NUM_NEURONS ",len(weights[0][0]), file=src);
    print("#define NUM_SYNAPSE ",len(weights[0]),file=src);
    print("#define FRAME_IN frame_"+str(layer_id)+".val",file=src);
    if (layer_id == len(model.layers)):
        print("#define FRAME_OUT final_frame.val",file=src);
    else:
        print("#define FRAME_OUT frame_"+str(layer_id+1)+".val",file=src);

    # WEIGHT ARRAY
    print("REAL w_"+str(layer_id)+"[NUM_NEURONS*NUM_SYNAPSE] = {", file=src);
    for j in range(len(weights[0][0])):
        for i in range(len(weights[0])):
            if (i == 0 and j == 0):
                print(weights[0][i][j],end='',file=src);
            else:
                print(",", weights[0][i][j],end='',file=src);
    print("};",file=src);

    # BIAS ARRAY
    print("REAL b_"+str(layer_id)+"[NUM_NEURONS] = {", file=src);
    for j in range(len(weights[0][0])):
            if (j == 0):
                print(weights[1][j],end='',file=src);
            else:
                print(",", weights[1][j],end='',file=src);
    print("};",file=src);        
    src.close();

    layer_name = "cpu_"+str(layer_id);
    src = open("cpu_"+str(layer_id)+".c", "w");
    print("#include \"" + layer_name + ".h\"" ,file=src);
    print("void process" + str(layer_id) + "()" ,file=src);
    print("{" ,file=src);
    print("int neu,syn;",file=src);
    print("for (neu = 0; neu != NUM_NEURONS; neu++) {", file=src);
    print("double sum = BIAS [neu];",file=src);
    print("for (syn = 0; syn != NUM_SYNAPSE; syn++) ", file=src);
    print("sum += (WEIGHT [syn+neu*NUM_SYNAPSE] * FRAME_IN [syn]);", file=src);
    print("FRAME_OUT [neu] = max(0.0,sum);", file=src);
    print("}", file=src);
    print("}" ,file=src);        
    src.close();
    
print('Test loss:', score[0])
print('Test accuracy:', score[1])
