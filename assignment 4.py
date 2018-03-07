import hashlib, os, time


		
class Main_Program():
    def get_hash_of_binary_file_contents (self, file_path, algorithm='MD5'):
      """This function will read and hash the contents of a file. 
      
      :param file_path: The path to the file to be hashed.
      :type file_path: str.
      :param algorithm: The hashing algorithm to be used. Defaults to 'MD5'.
      :type algorithm: str.
      :returns: str -- The hash of the contents of the file.
      """
      file_contents = self.read_binary_file(file_path)
      file_hash = self.get_hash_of_string(file_contents, algorithm)
      return file_hash

    def get_hash_of_string (self, string, algorithm='MD5'):
      if algorithm == 'MD5': #fixed spelling error, changed algorith to algorithm
        hash_object = hashlib.md5(string.encode()) #encoded the string, unicode-objects need to be encoded before hashing
        hash_digest = hash_object.hexdigest()
      else:
        hash_digest = ''
      return hash_digest

    def read_binary_file (self, file_path): # I got rid of the try/except. It's a resource intensive command on the processor and invalid file paths are taken care of in my functions
        file_object = open(file_path,'r') #Here I changed 'rb' to 'r' so the file could be read
        file_contents = file_object.read()
        file_object.close()
        return file_contents

    def get_hash_of_file(self): #This function creates a hash of a single file and saves it to a text file, has a loop to choose multiple single files
        print("Hash values will be saved to a file called 'file_hash_list.txt'")
        path_to_hash = input("Input the path of the file to hash (Need entire path, ex C:\...), type 'Back' to return to the main line: ") #Input for the user to specify the file path
        while path_to_hash != "Back": #This loop allows multiple files to be hashed while also allowing the user to exit the loop when finished hashing files
            if os.path.isfile(path_to_hash): #Prevents the program from crashing if the file doesn't exist
                hashed_file = self.get_hash_of_binary_file_contents(path_to_hash)
                print(hashed_file)
                file_hash_list = open("file_hash_list.txt", "a") #opens the text file to be edited
                file_hash_list.write("The hash of " + path_to_hash + " is " + hashed_file + "\r\n") #Writes the hash to our text file
                file_hash_list.close() #Need to close the text file so changes are saved
            else:
                print("File path does not exist.")
            path_to_hash = input("Input another file to hash, type 'Back' to return to the main line: ") #Allows the user to specify if he/she wants to hash another file

    def get_hash_of_folder(self): #This function creates a hash of every binary file inside a folder, has a loop to choose multiple folders
        print("Hash values will be saved to a file called 'folder_hash_list.txt'")
        folder_path = input("Input the path of the folder to hash, or 'Back' to return to the main line: ") #Specifies the folder path
        while folder_path != "Back":
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    Folder_Plus_Filename = folder_path + '/' + filename #Creates a variable storing the path of each file in the folder
                    if os.path.isfile(Folder_Plus_Filename): #This loop hashes each file in the folder
                        hashed_files = self.get_hash_of_binary_file_contents(Folder_Plus_Filename)
                        print("The hash for " + filename + " is " + hashed_files) #I made sure to put the file hash next to the file name to avoid confusion
                        folder_hash_list = open("folder_hash_list.txt", "a")
                        folder_hash_list.write("The hash for " + filename + " is " + hashed_files + "\r\n")#"\r\n" breaks the hashes into seperate lines for ease of reading
                        folder_hash_list.close()

            else:
                print("This directory does not exist")
            folder_path = input("Input the path to another folder to hash, or 'Back' to return to the main line: ")

    def hash_created_files(self): #This function creates a third hash file which contains a hashes of the 'File hash' and 'Folder hash' text files
        hashed_file = self.get_hash_of_binary_file_contents("file_hash_list.txt")
        hashed_folder = self.get_hash_of_binary_file_contents("folder_hash_list.txt")
        hash_hash_list = open("hash_of_hashes.txt", "a")
        hash_hash_list.write("The hash for 'file_hash_list.txt' is " + hashed_file + "\r\n" + "The hash for 'folder_hash_list.txt' is " + hashed_folder)
        hash_hash_list.close()
                
    def check_if_files_exist(self): #This function checks if the files being used already exist and creates them if they don't
        Valid_File_Hash = os.path.isfile("file_hash_list.txt") #These three lines set True/False values to the existence of the files the program uses
        Valid_Folder_Hash = os.path.isfile("folder_hash_list.txt")
        Valid_Hash_Hash = os.path.isfile("hash_of_hashes.txt")
        if Valid_File_Hash and Valid_Folder_Hash and Valid_Hash_Hash: #This loop either allows the program to continue if the files exist and creates them if they don't
            print("Loading from previously created files...")
        else:
            if Valid_File_Hash == False: #Here I use three "if" statements rather than an If/Elif/Else because all three must be read to assure all three files exist
                file_hash_list = open("file_hash_list.txt", "w")
                file_hash_list.close()
            if Valid_Folder_Hash == False:
                folder_hash_list = open("folder_hash_list.txt", "w")
                folder_hash_list.close()
            if Valid_Hash_Hash == False:
                hash_hash_list = open("hash_of_hashes.txt", "w")
                hash_hash_list.close()
            print("Creating hash text files...")
            
    def compare_hash_strings(self): #This funtion compares two files to see if they have the same hash or not
        file_one = input("Input the path of the first file: ")
        file_two = input("Input the path of the second file: ")
        if os.path.isfile(file_one) and os.path.isfile(file_two): #This if statement stops the program from crashing if one/both of the file paths doesn't exist
            hashed_file_one = self.get_hash_of_binary_file_contents(file_one)
            hashed_file_two = self.get_hash_of_binary_file_contents(file_two)
            if hashed_file_one == hashed_file_two:
                print("The files have the same hash")
            elif hashed_file_one != hashed_file_two:
                print("The files have different hashes")
        else:
            print("One or both of your directories does not exist.")

    def main_function(self): #This function ties the hashing file and hashing folder functions together
        self.check_if_files_exist() #Checks if the text files being used exist or not, creates them if they don't
        run_program = True
        while run_program == True: #This creates a loop which prevents the program from closing until our user desires it to
            input_choice = input("Type 'File' to hash a file, 'Folder' to hash files within a folder, or 'Next' for more options(Capitalization matters!): ") #Allows the user to specify if he/she wants to hash single files or a folder of files
            if input_choice == "File":
               self.get_hash_of_file()
            elif input_choice == "Folder":
               self.get_hash_of_folder()
            elif input_choice == "Next":
                hash_or_close = input("Type 'Compare' to compare the hash of two files, 'Hash' to create a hash text file out of the file hash and folder hash text files or 'Quit' to exit: ")
                if hash_or_close == "Hash":
                    self.hash_created_files()
                    print("hash_of_hashes.txt created. Program will close in 5 seconds.")
                    time.sleep(5) #The sleep command gives the user time to read that the command went through and ends the program without asking him/her to type another command to quit
                    run_program = False
                elif hash_or_close == "Compare":
                    self.compare_hash_strings()
                elif hash_or_close == "Quit":
                    run_program = False

prog = Main_Program()
prog.main_function() #Calling on this function begins the program

import unittest

class Unit_Tests(unittest.TestCase): #This class tests the three original functions

	def test_read_binary_file(self): #This function makes sure that the read_binary_file function does not have a FileNotFoundError
		try:
			Main_Program().read_binary_file("Hash Program.py")
		except FileNotFoundError:
			return self.fail("read_binary_file() raised FileNotFoundError unexpectedly!")
	
	def test_get_hash_of_binary_file_contents(self): #This function makes sure that the file selected does not have a UnicodeDecodeError
		try:
			Main_Program().get_hash_of_binary_file_contents("Hash Program.py")
		except UnicodeDecodeError:
			return self.fail("read_binary_file() raised UnicodeDecodeError unexpectedly!")
			
	def test_get_hash_of_string(self): #This test creates a hash of the string "test" and compares it to an already generated hash of the same string
		return self.assertEqual("098f6bcd4621d373cade4e832627b4f6", Main_Program().get_hash_of_string("test"))

if __name__ == '__main__': #This if statement runs the tests
    unittest.main()
