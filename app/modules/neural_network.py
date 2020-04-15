import copy
import numpy as np


class NeuralNetwork:
    def __init__(self, inputs=1, hidden_layers=1, hidden_neurons=1, outputs=1):
        self.inputs = inputs
        self.hidden_layers_number = hidden_layers
        self.hidden_neurons_number = hidden_neurons
        self.outputs_number = outputs

        # Create the layers
        self.inputs_layer = np.zeros((1, inputs))
        self.outputs_layer = np.zeros((1, outputs))
        self.hidden_layers = np.zeros((hidden_layers, 1, hidden_neurons))

        self.weights = []
        self.biases = []

        # Create the hidden layers

        for i in range(hidden_layers + 1):
            self.biases.append(np.random.uniform(-1.0, 1.0))

            # Check if its the first set of weights
            if i == 0:
                # This line adds a randmized 2d array of a certain shape
                self.weights.append(
                    np.random.uniform(-1, 1, (inputs, hidden_neurons))
                )
            elif i == len(self.hidden_layers):
                self.weights.append(
                    np.random.uniform(-1, 1, (hidden_neurons, outputs))
                )
            else:
                self.weights.append(
                    np.random.uniform(-1, 1, (hidden_neurons, hidden_neurons))
                )

    def show(self):
        print(self.inputs_layer.shape, end='---')

        for i in range(len(self.hidden_layers)):
            print('weights:', self.weights[i].shape, end='---')
            print('hidden: ', self.hidden_layers[i].shape, end='---')

        print('weights: ', self.weights[-1].shape, end='---')
        print(self.outputs_layer.shape,  end='---')

        print('')

    def copy(self, neural_network):
        self.weights = copy.deepcopy(neural_network.weights)
        self.biases = copy.deepcopy(neural_network.biases)

        return self

    def merge(self, parent_1, parent_2, mutation_rate=0.5):
        for i in range(self.hidden_layers_number + 1):
            if np.random.uniform(0, 1) < mutation_rate:
                self.biases[i] = np.random.uniform(-1.0, 1.0)
            else:
                if np.random.uniform(0, 1) > .5:
                    self.biases[i] = parent_1.biases[i]
                else:
                    self.biases[i] = parent_2.biases[i]

            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    if np.random.uniform(0, 1) < mutation_rate:
                        self.weights[i][j][k] = np.random.uniform(-1.0, 1.0)
                    else:
                        if np.random.uniform(0, 1) > .5:
                            self.weights[i][j][k] = parent_1.weights[i][j][k]
                        else:
                            self.weights[i][j][k] = parent_2.weights[i][j][k]

    def predict(self, inputs):
        self.inputs_layer = np.tanh(inputs.copy())

        self.hidden_layers[0] = np.tanh(
            self.inputs_layer.dot(self.weights[0]) + self.biases[0])

        for i in range(1, len(self.hidden_layers)):
            self.hidden_layers[i] = np.tanh(
                self.hidden_layers[i - 1].dot(self.weights[i]) + self.biases[i])

        self.outputs_layer = np.tanh(
            self.hidden_layers[-1].dot(self.weights[-1]) + self.biases[-1])

        return self.outputs_layer.copy()
