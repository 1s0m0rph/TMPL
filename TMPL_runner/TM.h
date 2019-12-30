//
// Created by Isomorph on 12/30/19.
//

#ifndef TMPL_RUNNER_TM_H
#define TMPL_RUNNER_TM_H

using namespace std;
#include <string>
#include <map>
#include <tuple>

enum direction{LEFT,RIGHT};

class TM
{
	public:
		TM(string *_alphabet, int _num_input_symbols, string *_tape_alphabet, int _num_symbols, int _num_states);
		bool simulate(string input);
		void add_transition(int from_state, string on_symbol, int to_state, string write_symbol, direction mvdir);

		const string LEFT_ENDMARKER = "<";
		const string RIGHT_ENDMARKER = ">";
		const string BLANK_CHAR = "_";
		const int START_STATE = -1;
		const int ACCEPT_STATE = -2;
		const int REJECT_STATE = -3;

	private:
		string* alphabet;
		string* tape_alphabet;
		int num_input_symbols;
		int num_symbols;
		int num_states;
		tuple<int,string,direction>** transition_function;
		map<string,int> symbol_map;//maps symbols (e.g. 'aR') onto ints in the range [0,number of symbols)

		int get_state_index(int state);
};


#endif //TMPL_RUNNER_TM_H
