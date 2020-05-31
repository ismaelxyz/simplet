// regex_search(input, sm, regex("([a-z]+).*(->).*[^a-z]([a-z]+)")) // # as -> fr\n
// (".*(->).*[^a-z]([a-z]+)" // "# -> en\n"
// "([a-z]+).*(->).*" // "# en -> "
// "([].*)//" // "sopa // asd"

static PyObject* PyChars_ClearComment(string text) {
  // Comment type //
  string n_text = "";
  bool swich = false;

  for (int i = 0; i != text.size(); ++i) {
    i += 3;
    if (text[i] == "/"[0]) {
      if (text[i + 1] == "*"[0]) {
        swich = true;
      
      } else if (text[i - 1] == "*"[0] && swich) {
        swich = false;
        continue;
      
      } else if (text[i + 1] == "/"[0]) {
        break;
      
      } else if (text[i + 1] != "/"[0] && swich) {
        continue;
     
      } else {
        // Syntax Error
        exit(1);
      }

    } 
    if (!swich) { n_text += text[i]; }
    
  }
  if (swich) { 
    // swich never change to false.
    exit(1); 
  }

  return Py_BuildValue("s", n_text);
}

int main(){
string input = "# es0 -> en\n";
  // cout << input << endl;
  smatch sm;
  
  /* 
    If input ends in a quotation that contains a word that begins with "reg"
     and another word beginning with "ex" then capture the preceding portion of input
  */
  if (input[0] == "#"[0]) {
    // [a-zA-Z0-9_]
    if (regex_search(input, sm, regex("([a-z]+).*(->).*[^a-z]([a-z]+)"))) {
      // re.search("([a-z]*.).->.(.*[a-z])", "# es -> en\n").group(2)
      // re.search("(\w+).*(->).*[^\w+](\w+)", "#   es   -> en\n").group(3)
      cout << sm[0] << "\n" << sm[1] << "\n" << sm[2] << "\n" << sm[3] << "\n" << sm.size();
    } else {
       cout << "not";
    }
  }
  /*
  if (regex_match(input, sm, regex("(.*)\".*\\breg.*\\bex.*\"\\s*$"))) {
    const auto capture = sm[1].str();
    cout << '\t' << capture << endl; // Outputs: "\tSome people, when confronted with a problem, think\n"
    cout << sm[0].str() << "->es" << endl;
    // Search our capture for "a problem" or "# problems"

    if(regex_search(capture, sm, regex("(a|d+)\\s+problems?"))) {
      const auto count = sm[1] == "a"s ? 1 : stoi(sm[1]);
      cout << '\t' << count << (count > 1 ? " problems\n" : " problem\n"); // Outputs: "\t1 problem\n"
      cout << "Now they have " << count + 1 << " problems.\n"; // Outputs: "Now they have 2 problems\n"
    }
  }
  */
  return 0;
}