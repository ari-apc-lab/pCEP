/*
 * Copyright (C) 2019  Atos Spain SA. All rights reserved.
 *
 * This file is part of pCEP.
 *
 * pCEP is free software: you can redistribute it and/or modify it under the
 * terms of the Apache License, Version 2.0 (the License);
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * The software is provided "AS IS", without any warranty of any kind, express or implied,
 * including but not limited to the warranties of merchantability, fitness for a particular
 * purpose and noninfringement, in no event shall the authors or copyright holders be
 * liable for any claim, damages or other liability, whether in action of contract, tort or
 * otherwise, arising from, out of or in connection with the software or the use or other
 * dealings in the software.
 *
 * See README file for the full disclaimer information and LICENSE file for full license
 * information in the project root.
 *
 * Authors:  Atos Research and Innovation, Atos SPAIN SA
 */

/* 
	Compiler framework for Dolce
*/
#ifndef _SOL_CEP_COMPILER_CONTEXT_H_
#define _SOL_CEP_COMPILER_CONTEXT_H_
 
class Parser;

/*!
	\brief Context used to operate multiple instances 
		of lex/yacc parsers in a thread safe manner.
		
	Based on information found in:
	
	http://www.lemoda.net/c/reentrant-parser/index.html
	
*/
struct ParserContext
{
	void* scanner;
	
	Parser* parser;
	
	int line;
	int col;
};


#endif 

