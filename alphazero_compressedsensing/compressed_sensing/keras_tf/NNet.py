from CS_NNet import NetArch
import numpy as np
from keras.models import Model, model_from_json

class NNetWrapper(): 
	#Game_args is an object, while args is just a dictionary found in main.py. When we initialize a 
	#NNetWrapper object, we specify these two args from main.py and Game_Args.py
	def __init__(self, args, Game_args): 
		self.args = args
		self.nnet = NetArch(args, Game_args) #self.nnet is a NetArch object
	
	def constructTraining(states): #this method is used in Coach.py
	#INPUT: a list or deque of state objects which have values for self.feature_dic, self.p_as, and self.z
	#OUTPUT: (X,Y) training data saved into .csv file. Ideally for training, we would just directly read in from .csv file if
	#necessary
	#NOTE: Do not use state.nn_input, since constructing state.nn_input for each state takes additional time. Training (X,Y)
	#is directly constructed from state.feature_dic. nn_input should only be used for NNetWrapper.predict. 
		num_states = len(states)
		X = []
		Y = []
		#Initialize every entry in X as an empty numpy array matrix		
		list_index = 0
		for key in states[0].feature_dic: #Each state's feature dictionary should contain vectors which are all the same size
			X[list_index] = np.empty((num_states,len(states[0].feature_dic[key])))
			list_index += 1
	
		#Fill in each empty numpy array in X
		for i in range(num_states): #iterate over the number of states, which is equal to the row dim of every np array in X.
			list_index = 0
			for key in states[i].feature_dic:
				X[list_index][i][:] = states[i].feature_dic[key] 
				list_index += 1	
				
		#Construct labels Y, which is length 2 list of numpy arrays
		pi_as_empty = np.empty((num_states, states[0].action_indices.size))
		z_empty = np.empty((num_states,))
		Y.append(pi_as_empty)
		Y.append(z_empty)
			
		for i in Y[0].shape[0]: #Y[0].shape equals number of states
			Y[0][i][:] = states[i].pi_as
		for i in Y[1].shape[0]:
			Y[1][i] = states[i].z
		
		converted_training = [X, Y]
		return converted_training
			
	def train(self, X, Y): 
	#INPUT: A list, where each element in the list is itself a list of self play games. 
	#Each element in this embedded list is in the form [X,Y], which contains all the data for a single
	#self-pair game. 
	#OUTPUT: updated class variable self.nnet
		
		self.nnet.model.fit(X,Y, epochs = self.args['epochs'], batch_size = self.args['batch_size'])
		
	def predict(self, state): 
	#INPUT: state object. Note that state.col_indices, state.feature_dic and state.converttoNNInput 
	#must all be computed before NNetWrapper.predict can make a meaningful prediction. 
	#OUTPUT: p_as and v
		
		p_as, v = self.nnet.model.predict(state.nn_input)	
		return p_as, v
	
	def save_checkpoint(self, folder, filename):
	#INPUT: folder and filename 
	#OUTPUT: None
	#FUNCTION: save the current model and its weights in some folder
		self.nnet.model.save_weights(folder + filename + '_weights.h5')
		model_json = self.nnet.model.to_json()
		with open(folder + filename + '_model.json', 'w') as json_file:
			json_file.write(model_json)
			
	def load_checkpoint(self, folder, filename):
	#INPUT: folder and filename
	#OUTPUT: load a model and its weights with given folder and filename into self.nnet
		#Load the model
		json_file = open(folder + filename + '_model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self.nnet.model = model_from_json(loaded_model_json)
		#Load the weights
		self.nnet.model.load_weights(folder + filename + '_weights.h5')
		