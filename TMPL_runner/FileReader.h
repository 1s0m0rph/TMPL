//
// Created by Isomorph on 12/30/19.
//

#ifndef TMPL_RUNNER_FILEREADER_H
#define TMPL_RUNNER_FILEREADER_H

#include "TM.h"

class FileReader
{
	public:
		TM create_from_file(string filename);
	private:
		char* encoding;
		int encoding_length;
		int encoding_index;//bit index, so index in the encoding array is this >> 3
		TM M;//this is what we're building
		string* alphabet;
		int input_alphabet_size;
		string* tape_alphabet;
		int alphabet_size;
		int num_states;
		int symbol_encoding_width;
		int state_encoding_width;

		char* read_next_n_bits();
		void read_preprocessor_numbers();//read in the version number and number of states
		void read_alphabets();//read in both alphabets (reading the input alphabet as a subset of the tape alphabet
		void read_transition_function();
};


#endif //TMPL_RUNNER_FILEREADER_H
