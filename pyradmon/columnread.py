#!/usr/bin/env python
# PyRadmon - Python Radience Monitor Tool
# Copyright 2014 Albert Huang.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Column Reader Library - 
#   library for reading column (and subcolumn) headers, and figuring
#   out the column indexes for the raw data
# 

class ColumnReadBase():
    """Base class for column readers.

    This is the base class for column readers. It implements the base
    methods and sets the base variables up for future use.
    
    A column dictionary is created for the column reader::
    
        { 
            'COLUMN_NAME': {
                       'name'       : 'COLUMN_NAME',  # Column name
                       'column_id'  : NNN,            # Column index
                       'subcolumns' : [               # Subcolumn names
                                       'SUBCOLUMN_NAME',
                                       'SUBCOLUMN_NAME',
                                      ],
                       }
        }

    Attributes:
        data (str): The raw string data for the columns.
        column_dict (dict): The column dictionary created from the raw
            string data.
        unique_char (str): A string indicating a character that is 
            unlikely to be used in a column name. This is usually one 
            character in length, and is usually the column delimiter.
        max_col_levels (int): An integer representing the maximum 
            number of column levels possible. Note that the functions 
            in this class are only designed to handle a maximum of 2 
            levels. Adding more levels will require rewriting the data 
            processing and the fetching functions!
    
    """
    def __init__(self, data):
        """Initializes ColumnReadBase with raw string data "data"."""
        
        # Initial variables!
        
        self.data = data
        self.column_dict = self._process_data()
        self._validate()
        
        # This should be set to a character that is unlikely to be used in
        # a column name. The delimiter character is best for this.
        
        self.unique_char = "|"
        
        # Maximum number of column levels
        # Note that the functions in this class are only designed to handle
        # a maximum of 2 levels. Adding more levels will require rewriting
        # the data processing and the fetching functions!
        
        self.max_col_levels = 2
        
        # This call, if subclassed and changed, will alter or set additional
        # variables. Therefore, all initial variables need to be set before
        # this line!
        
        self._set_settings()
        
    def _validate(self):
        # Data structure validation function.
        # Override this function if the data structure changes.
        # The function should only raise errors. If no errors, do nothing.
        
        if type(self.column_dict) == dict:
            for key in self.column_dict:
                if not ( 
                         ('column_id' in self.column_dict[key]) and 
                         ('subcolumns' in self.column_dict[key]) and 
                         ('name' in self.column_dict[key])
                       ):
                    raise Exception("ERROR: Data structure for columns are invalid!")
                else:
                    if type(self.column_dict[key]['subcolumns']) != list:
                        raise Exception("ERROR: Data structure for columns are invalid! (subcolumns are not a list!)")
    def _process_data(self):
        # Data processing function
        # This function should be overrided to adapt to the desired
        # data. Not overriding this function will cause an error to
        # occur. The function should read self.data to create a
        # self.column_dict.
        # 
        # Desired structure:
        # { 
        #     'COLUMN_NAME': {
        #                'name'            : 'COLUMN_NAME',
        #                'column_id'       : NNN,
        #                'subcolumns'      : [
        #                                     'SUBCOLUMN_NAME',
        #                                     'SUBCOLUMN_NAME',
        #                                    ],
        #                }
        # }
        # 
        # Note that the above structure is invalid if you decide to
        # add more levels or decide to change the structure of
        # self.column_dict.
        # 
        
        print "ERROR: You should NOT use this class, since it doesn't do anything."
        print "_process_data() is unimplemented..."
        raise Exception("ERROR: Class method _process_data() not overrided!")
        return {}
        
    def _set_settings(self):
        # This function should be overriden if any initial variables
        # need to be changed, or if any methods need to be run.
        pass
        
    def _warn(self, msg):
        # Warning printing function
        print "getColumnID(): WARNING: "+msg
    
    def getColumnDict(self):
        """Return the internal column dictionary.
        
        Return the internal column dictionary that the object currently
        has.
        
        Args:
            None
        
        Returns:
            dict: A dictionary representing the column structure 
            detected by the column reader. General structure::
            
                { 
                   'COLUMN_NAME': {
                       'name'       : 'COLUMN_NAME',  # Column name
                       'column_id'  : NNN,            # Column index
                       'subcolumns' : [               # Subcolumn names
                                       'SUBCOLUMN_NAME',
                                       'SUBCOLUMN_NAME',
                                      ],
                   }
                }
        
        """
        return self.column_dict
    
    def getColumnIndex(self, col_search_name, suppress_warnings = True):
        """Based on the column parsing, determine the column index
        given the column name.

        Fetches the column index from the column parsing dictionary,
        given the column name (and optionally, the subcolumn name).

        Args:
            col_search_name (str): The name of the column, and 
                optionally, the subcolumn name. If specifying a 
                subcolumn, the format should look like 
                "COLUMN_NAME!SUBCOLUMN_NAME", where the ! is the 
                delimiter set in self.unique_char. By default, the 
                delimiter is a pipe character, '|'.
            suppress_warnings (bool): A boolean indiciating whether to
                suppress warnings or not. By default, this is set to
                True.

        Returns:
            int or None: An integer representing the column index of 
            the specified column (and optionally, subcolumn). If 
            nothing found, this will return None. 

        Note:
            Warnings will be printed, if enabled. It is up to the 
            receiving end to detect None returns.
        
        """
        # Format of name:
        # COL_NAME
        # COL_NAME|SUBCOL_NAME
        
        ## Sanity check
        # Check for blank col_name
        if len(col_search_name.strip()) == 0:
            if not suppress_warnings:
                self._warn("Column name is blank! Returning None.")
            return None
        
        # Check for self.column_dict init
        if not hasattr(self, 'column_dict'):
            if not suppress_warnings:
                self._warn("self.column_dict not initialized yet! Returning None.")
            return None
        
        # Check for valid unique_char
        if self.unique_char == " " or self.unique_char == "":
            if not suppress_warnings:
                self._warn("self.unique_char is not valid! It can't be empty or be a space! Returning None.")
            return None
        
        # Split it apart!
        col_split = col_search_name.split(self.unique_char)
        
        col_name = col_split[0]
        
        ## More sanity checks!
        
        # Check for length
        if (len(col_split) == 0) or (len(col_split) > self.max_col_levels):
            if not suppress_warnings:
                self._warn("Invalid amount of column levels! (Detected levels: %i) Returning None." % len(col_split))
            return None
        
        # Check for valid column
        if not col_name in self.column_dict:
            if not suppress_warnings:
                self._warn("'%s' is not a valid column! Returning None." % col_name)
            return None
        
        # Check to see if we have any subcolumns.
        if len(self.column_dict[col_name]['subcolumns']) > 0:
            if len(col_split) == 1:
                if not suppress_warnings:
                    self._warn("Column has subcolumns, but args only specify the column. Will return the column ID, defaulting to first subcolumn.")
                return self.column_dict[col_name]['column_id']
            else:
                if col_split[1] in self.column_dict[col_name]['subcolumns']:
                    # Return the column ID + rel index of subcol
                    return self.column_dict[col_name]['column_id'] + self.column_dict[col_name]['subcolumns'].index(col_split[1])
                else:
                    # No good.
                    if not suppress_warnings:
                        self._warn("Could not find subcolumn '%s' in column '%s'! Returning None." % (col_split[1], col_split[0]))
                    return None
        else:
            # Just a column, nothing more.
            if len(col_split) == 1:
                return self.column_dict[col_name]['column_id']
            else:
                # There's no subcolumn... so return error.
                if not suppress_warnings:
                    self._warn("Column '%s' does not have any subcolumns! Returning None." % (col_split[0]))
                return None

# Columns with pipes!
# Table structure looks like:
#    !hello |   hi | helloooooooooo |      maybe
#    !      |      |     hi    byee |           
#     1.23    234   123455   12519   12419239.2
class ColumnReadPipes(ColumnReadBase):
    """Subclass of ColumnReadBase, processing columns delimited with
    pipes. The table structure looks like::
    
        !hello |   hi | helloooooooooo |      maybe
        !      |      |     hi    byee |           
          1.23    234   123455   12519   12419239.2
    
    This subclass overrides the _process_data method to set up the
    self.column_dict structure.
    """
    
    def _process_data(self):
        data = self.data
        data_lines = data.split("\n")
        # Desired structure:
        # { 
        #     'COLUMN_NAME': {
        #                'name'            : 'COLUMN_NAME',
        #                'column_id'       : NNN,
        #                'subcolumns'      : [
        #                                     'SUBCOLUMN_NAME',
        #                                     'SUBCOLUMN_NAME',
        #                                    ],
        #                }
        # }
        COLUMNS = None
        SUBCOLUMNS = None
        for data_line in data_lines:
            # Skip blank lines.
            if data_line.strip() == "":
                continue
            # Once we encounter a non-commented line (no !), break.
            if data_line[0] != "!":
                break
            else:
                data_line = data_line[1:]
                if COLUMNS == None:
                    COLUMNS = data_line.split("|")
                elif SUBCOLUMNS == None:
                    SUBCOLUMNS = data_line.split("|")
                else:
                    raise Exception("ERROR: Too many comments for columns field!")
        
        # Sanity check
        if COLUMNS == None:
            raise Exception("ERROR: Could not process columns!")
        if SUBCOLUMNS == None:
            raise Exception("ERROR: Could not process subcolumns!")        
        
        # Clean the columns up
        COLUMNS = [COLUMN.strip() for COLUMN in COLUMNS]
        SUBCOLUMNS = [SUBCOLUMN.strip() for SUBCOLUMN in SUBCOLUMNS]
        
        # Sanity check!
        if len(COLUMNS) != len(SUBCOLUMNS):
            raise Exception("ERROR: Different number of columns vs subcolumns (%i vs %i)!" % (len(COLUMNS), len(SUBCOLUMNS)))
        
        # Connect columns to subcolumns (and vice versa)
        # [ "Hello", "Hello 2", "Hello 3", "Hello 4", "Hello 5", ""     ]
        # [ ""     , "Hi"     , ""       , ""       , "Hi 5"   , "Hi 6" ]
        PREV_COLUMN = ""
        SUBCOLUMN_DICT = {}
        for i in xrange(0, len(COLUMNS)):
            if COLUMNS[i] == "":
                if SUBCOLUMNS[i] != "":
                    if not PREV_COLUMN in SUBCOLUMN_DICT:
                        SUBCOLUMN_DICT[PREV_COLUMN] = []
                    SUBCOLUMN_DICT[PREV_COLUMN].append(SUBCOLUMNS[i])
                else:
                    # This is weird...
                    pass
            else:
                if SUBCOLUMNS[i] != "":
                    if not COLUMNS[i] in SUBCOLUMN_DICT:
                        SUBCOLUMN_DICT[COLUMNS[i]] = []
                    SUBCOLUMN_DICT[COLUMNS[i]].append(SUBCOLUMNS[i])
                else:
                    # Do nothing!
                    pass
            
            if COLUMN != "":
                PREV_COLUMN = COLUMNS[i]
        
        # Build final dict!
        FINAL_COLUMN_DICT = {}
        COLUMN_DICT = {}
        COLUMN_ID = 0
        for COLUMN in COLUMNS:
            COLUMN_DICT = {}
            #print "COLUMN %s set to COLUMN_ID %i" % (COLUMN, COLUMN_ID)
            COLUMN_DICT['name'] = COLUMN
            COLUMN_DICT['column_id'] = COLUMN_ID
            if COLUMN in SUBCOLUMN_DICT:
                COLUMN_DICT['subcolumns'] = SUBCOLUMN_DICT[COLUMN]
                COLUMN_ID += len(SUBCOLUMN_DICT[COLUMN]) - 1
            else:
                COLUMN_DICT['subcolumns'] = []
            
            if COLUMN != '':
                FINAL_COLUMN_DICT[COLUMN] = COLUMN_DICT
                COLUMN_ID += 1
        
        #pprint.pprint(FINAL_COLUMN_DICT)
        return FINAL_COLUMN_DICT
            
# WIP!
# This is pretty much done - however, support for spaces in subcolumns is not
# implemented (yet). To implement, follow the same steps as before with columns.
class ColumnReadSpaces(ColumnReadBase):
    """Subclass of ColumnReadBase, processing columns delimited with
    spaces. The table structure looks like::
    
        !hello     hi   helloooooooooo        maybe
        !                   hi    byee             
          1.23    234   123455   12519   12419239.2
    
    This subclass overrides the _process_data method to set up the
    self.column_dict structure.
    
    NOTE:
        This is pretty much done. However, support for spaces in 
        subcolumns is not implemented (yet). To implement, follow the 
        same steps as before with columns in the code below.
    """
    def _process_data(self):
        data = self.data
        data_lines = data.split("\n")
        i = 0
        # Desired structure:
        # { 
        #     'COLUMN_NAME': {
        #                'name'            : 'COLUMN_NAME',
        #                'column_id'       : NNN,
        #                'subcolumns'      : [
        #                                     'SUBCOLUMN_NAME',
        #                                     'SUBCOLUMN_NAME',
        #                                    ],
        #                }
        # }
        # How to do it? Look at table, mark 1 if it has a letter, 0 if it's a
        # space. Then look for columns that are all zeroes. 
        
        LINE_NUM_START = 0
        for line in data_lines:
            if line == '':
                LINE_NUM_START += 1
                continue
            break
        
        BINARIZED_DATA = []
        BINARIZED_DATA_LINE = []
        
        BINARIZED_DATA_NO_COMMENTS = []
        BINARIZED_DATA_NO_COMMENTS_LINE = None
        LINE_TRACK = 0
        
        ## STEP 1: Binarize the file
        for data_line in data_lines:
            BINARIZED_DATA_LINE = []
            for char in data_line:
                if char == ' ':
                    BINARIZED_DATA_LINE.append(0)
                else:
                    BINARIZED_DATA_LINE.append(1)
            if len(BINARIZED_DATA_LINE) == 0:
                continue
            if data_line[0] != "!":
                if BINARIZED_DATA_NO_COMMENTS_LINE == None:
                    BINARIZED_DATA_NO_COMMENTS_LINE = LINE_TRACK
            else:
                LINE_TRACK += 1
            BINARIZED_DATA.append(BINARIZED_DATA_LINE)
        
        BINARIZED_DATA_NO_COMMENTS = BINARIZED_DATA[BINARIZED_DATA_NO_COMMENTS_LINE:]
        
        ## STEP 2a: Get max width!
        BINARIZED_DATA_MAX_WIDTH = 0
        for BINARIZED_DATA_LINE in BINARIZED_DATA:
            if len(BINARIZED_DATA_LINE) > BINARIZED_DATA_MAX_WIDTH:
                BINARIZED_DATA_MAX_WIDTH = len(BINARIZED_DATA_LINE)
        
        BINARIZED_DATA_MAX_HEIGHT = len(BINARIZED_DATA)
        
        BINARIZED_DATA_MAX_WIDTH_NO_COMMENTS = 0
        for BINARIZED_DATA_LINE in BINARIZED_DATA_NO_COMMENTS:
            if len(BINARIZED_DATA_LINE) > BINARIZED_DATA_MAX_WIDTH_NO_COMMENTS:
                BINARIZED_DATA_MAX_WIDTH_NO_COMMENTS = len(BINARIZED_DATA_LINE)
        
        BINARIZED_DATA_MAX_HEIGHT_NO_COMMENTS = len(BINARIZED_DATA_NO_COMMENTS)
        
        ## STEP 2b: Look for empty columns!
        #   X X X X
        # Y 1 0 1
        # Y 1 0 1 1
        # Y 1 0 1
        
        #print "MAX: (%i, %i)" % (BINARIZED_DATA_MAX_WIDTH, BINARIZED_DATA_MAX_HEIGHT)
        
        EMPTY_COLUMNS = []
        
        for X in xrange(0, BINARIZED_DATA_MAX_WIDTH):
            FOUND_EMPTY = True
            for Y in xrange(0, BINARIZED_DATA_MAX_HEIGHT):
                #print "Testing: (%i, %i) (size: %i, %i)" % (X, Y, len(BINARIZED_DATA[Y]), len(BINARIZED_DATA))
                #print BINARIZED_DATA[Y]
                if X >= len(BINARIZED_DATA[Y]):
                    #print "X exceeded in column Y=%i" % Y
                    break
                if BINARIZED_DATA[Y][X] == 1:
                    #print "Found 1, break"
                    FOUND_EMPTY = False
                    break
            if FOUND_EMPTY:
                EMPTY_COLUMNS.append(X)
                
        #pprint.pprint(EMPTY_COLUMNS)
        
        ## STEP 2c: Look for empty columns in value rows!
        EMPTY_COLUMNS_VALUES = []
        
        for X in xrange(0, BINARIZED_DATA_MAX_WIDTH_NO_COMMENTS):
            FOUND_EMPTY = True
            for Y in xrange(0, BINARIZED_DATA_MAX_HEIGHT_NO_COMMENTS):
                #print "Testing: (%i, %i)" % (X, Y)
                if Y > len(BINARIZED_DATA_NO_COMMENTS[Y]):
                    #print "X exceeded in column Y=%i" % Y
                    break
                if BINARIZED_DATA_NO_COMMENTS[Y][X] == 1:
                    #print "Found 1, break"
                    FOUND_EMPTY = False
                    break
            if FOUND_EMPTY:
                EMPTY_COLUMNS_VALUES.append(X)
                
        #pprint.pprint(EMPTY_COLUMNS_VALUES)
        
        ## STEP 3a: Cull by removing duplicate columns.
        ## We assume right justify, so we remove everything to the right with
        ## a difference of 1.
        OLD_VAL = EMPTY_COLUMNS[0]
        i = 1
        while i < len(EMPTY_COLUMNS):
            CUR_VAL = EMPTY_COLUMNS[i]
            #print "[i is %i] [CUR_VAL is %i]" % (i, CUR_VAL)
            if CUR_VAL - OLD_VAL == 1:
                #print "CUR_VAL purged by OLD_VAL diff 1: %i" % CUR_VAL
                EMPTY_COLUMNS.remove(CUR_VAL)
                i -= 1
            i += 1
            OLD_VAL = CUR_VAL
        
        #print "FILTERED:"
        #pprint.pprint(EMPTY_COLUMNS)
        #raw_input()
        
        ## STEP 3b: Cull by checking if consecutive points are blank (via
        ## EMPTY_COLUMNS_VALUES)
        
        # Build pairs
        i = 1
        while i < len(EMPTY_COLUMNS):
            # Pairs: (i - 1, i)
            VALUES_ARE_EMPTY = True
            #print "CHECK: %i to %i" % (EMPTY_COLUMNS[i - 1], EMPTY_COLUMNS[i])
            for j in xrange(EMPTY_COLUMNS[i - 1], EMPTY_COLUMNS[i]):
                if not j in EMPTY_COLUMNS_VALUES:
                    #print "  ** j=%i is non-empty, breaking." % j
                    VALUES_ARE_EMPTY = False
                    break
            if VALUES_ARE_EMPTY:
                #print "CUR_VAL purged by blank space cull: %i" % EMPTY_COLUMNS[i]
                EMPTY_COLUMNS.remove(EMPTY_COLUMNS[i])
                i -= 1
            i += 1
        
        # Insert the first column!
        EMPTY_COLUMNS.insert(0, 0)
        
        # Then set the last column to the last char of the line!
        # Exclude the dot...
        EMPTY_COLUMNS[-1] = len(data_lines[LINE_NUM_START]) - 1
        
        #print "FILTERED 2:"
        #pprint.pprint(EMPTY_COLUMNS)
        #raw_input()
        
        ## Now form final ACTUAL columns...
        FINAL_COLUMNS = []
        
        for i in xrange(1, len(EMPTY_COLUMNS)):
            FINAL_COLUMNS.append([EMPTY_COLUMNS[i-1], EMPTY_COLUMNS[i]])
        
        ## Then calculate subcolumns... not too bad.
        SUBCOLUMNS = []
        SC_START_POS = 0
        SC_END_POS = 0
        i = 1
        #print "Total data count: %i" % len(BINARIZED_DATA[1])
        while i < len(BINARIZED_DATA[1]):
            #print "i = %i" % i
            if BINARIZED_DATA[1][i] == 1:
                SC_START_POS = i
                for j in xrange(SC_START_POS, len(BINARIZED_DATA[1])):
                    if (BINARIZED_DATA[1][j] == 0) or (j == len(BINARIZED_DATA[1]) - 1):
                        SC_END_POS = j
                        break
                #print "Found SUBCOLUMN: %i -> %i" % (SC_START_POS, SC_END_POS)
                SUBCOLUMNS.append([SC_START_POS, SC_END_POS])
                i = SC_END_POS
            i += 1
            #print "NEW i = %i" % i
        
        ## More processing...
        NAME = ""
        
        COL_COUNT = 0
        COL_NAMES = []
        PREV_COL = []
        i = 0
        #for COL in FINAL_COLUMNS:
        while i < len(FINAL_COLUMNS):
            COL = FINAL_COLUMNS[i]
            NAME = ""
            for c in xrange(COL[0] + 1, COL[1]):
                #if BINARIZED_DATA[0][c] == 1:
                NAME += line[c]
            NAME = NAME.strip()
            
            if NAME == "":
                # Merge blank column with previous!
                NEW_COL = [PREV_COL[0], COL[1]]
                FINAL_COLUMNS = [NEW_COL if x==PREV_COL else x for x in FINAL_COLUMNS]
                FINAL_COLUMNS.remove(COL)
                i -= 1
            else:
                #print "Name for column %i: %s" % (COL_COUNT, NAME)
                COL_NAMES.append(NAME)
                COL_COUNT += 1
            
            PREV_COL = COL
            
            i += 1
        
        # Build subcolumn info
        
        SUBCOL_COUNT = 0
        SUBCOL_NAMES = []
        for SUBCOL in SUBCOLUMNS:
            SUBNAME = ""
            for c in xrange(SUBCOL[0], SUBCOL[1]+1):
                #if BINARIZED_DATA[0][c] == 1:
                SUBNAME += data_lines[LINE_NUM_START + 1][c]
            SUBNAME = SUBNAME.strip()
            #print "Name for subcolumn %i: '%s'" % (SUBCOL_COUNT, SUBNAME)
            SUBCOL_NAMES.append(SUBNAME)
            SUBCOL_COUNT += 1
        
        # Match up subcolumns with columns!
        
        COL_COUNT = 0
        SUBCOL_COUNT = 0
        SUBCOLUMN_DICT = {}
        for SUBCOL in SUBCOLUMNS:
            COL_COUNT = 0
            for COL in FINAL_COLUMNS:
                #print "Checking: Subcolumn %s in column %s (subc %i-%i, c %i-%i)" % (SUBCOL_NAMES[SUBCOL_COUNT], COL_NAMES[COL_COUNT], SUBCOL[0], SUBCOL[1], COL[0], COL[1])
                if (SUBCOL[0] >= COL[0]) and (SUBCOL[1] <= COL[1]):
                    #print " ** Subcolumn %s in column %s (subc %i, end c %i)" % (SUBCOL_NAMES[SUBCOL_COUNT], COL_NAMES[COL_COUNT], SUBCOL_COUNT, SUBCOL[1])
                    if COL_NAMES[COL_COUNT] not in SUBCOLUMN_DICT:
                        SUBCOLUMN_DICT[COL_NAMES[COL_COUNT]] = []
                    SUBCOLUMN_DICT[COL_NAMES[COL_COUNT]].append(SUBCOL_NAMES[SUBCOL_COUNT])
                    break
                COL_COUNT += 1
            SUBCOL_COUNT += 1
        
        ## Make the final ultimate column dictionary!
        FINAL_COLUMN_DICT = {}
        INDV_COLUMN_DICT = {}
        
        COLUMN_ID = 0
        
        for COL_NAME in COL_NAMES:
            FINAL_COLUMN_DICT[COL_NAME] = {}
            INDV_COLUMN_DICT = {}
            
            INDV_COLUMN_DICT["name"] = COL_NAME
            INDV_COLUMN_DICT["column_id"] = COLUMN_ID
            
            if (COL_NAME in SUBCOLUMN_DICT) and (len(SUBCOLUMN_DICT[COL_NAME]) > 0):
                INDV_COLUMN_DICT["subcolumns"] = SUBCOLUMN_DICT[COL_NAME]
                COLUMN_ID += len(SUBCOLUMN_DICT[COL_NAME]) - 1
            else:
                INDV_COLUMN_DICT["subcolumns"] = []
            
            FINAL_COLUMN_DICT[COL_NAME] = INDV_COLUMN_DICT
            
            COLUMN_ID += 1
        
        #pprint.pprint(FINAL_COLUMN_DICT)
        return FINAL_COLUMN_DICT
        
