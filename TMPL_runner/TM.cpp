//
// Created by Isomorph on 12/30/19.
//

#include <vector>
#include "TM.h"

TM::TM(string *_alphabet, int _num_input_symbols, string *_tape_alphabet, int _num_symbols, int _num_states)
{
	alphabet = _alphabet;
	tape_alphabet = _tape_alphabet;
	num_states = _num_states;
	num_input_symbols = _num_input_symbols;
	num_symbols = _num_input_symbols;

	//initialize the transition function
	transition_function = new tuple<int,string,direction>*[num_states];
	for(int i = 0; i < num_states; i++)
		transition_function[i] = new tuple<int,string,direction>[num_symbols];

	//initialize the symbol map
	for(int i = 0; i < num_symbols; i++)
		symbol_map[tape_alphabet[i]] = i;
}

bool TM::simulate(string input)
{
	vector<string> tape = vector<string>(input.size() + 2);
	tape.push_back(LEFT_ENDMARKER);
	for(char ch : input)
	{
		string add_str;
		add_str += ch;
		tape.push_back(add_str);
	}
	tape.push_back(RIGHT_ENDMARKER);

	int current_state = START_STATE;
	int read_head_loc = 1;

	while(current_state != ACCEPT_STATE && current_state != REJECT_STATE)
	{
		string read_symbol = tape[read_head_loc];
		int read_symbol_idx = symbol_map[read_symbol];
		int current_state_idx = get_state_index(current_state);
		tuple<int,string,direction> transition = transition_function[current_state_idx][read_symbol_idx];
		int to_state = get<0>(transition);
		string write_symbol = get<1>(transition);
		direction move_dir = get<2>(transition);

		tape[read_head_loc] = write_symbol;
		if(move_dir == LEFT)
		{
			read_head_loc--;
			if(read_head_loc < 0)
				read_head_loc = 0;
		}
		else if (move_dir == RIGHT)
		{
			read_head_loc++;
			if(read_head_loc >= tape.size())
				tape.push_back(BLANK_CHAR);
		}
		else
			throw invalid_argument("Unknown direction in TM::simulate");

		current_state = to_state;
	}

	return current_state == ACCEPT_STATE;
}

void TM::add_transition(int from_state, string on_symbol, int to_state, string write_symbol, direction mvdir)
{
	int from_state_idx = get_state_index(from_state);
	int on_symbol_idx = symbol_map[on_symbol];

	tuple<int,string,direction> add_transition = make_tuple(to_state,write_symbol,mvdir);
	transition_function[from_state_idx][on_symbol_idx] = add_transition;
}

int TM::get_state_index(int state)
{
	return (state < 0) ? (num_states + state) : state;//map -1 to the last one, -2 to the second-last, etc.
}
