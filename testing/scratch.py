from transformers import pipeline

# Create a zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

text = """Lab 4 CS265 Advanced Programming Tools and Techniques
2024-03-18T00:00:00+00:00
CS265
Assignment 1
Write a Bash script named indexer. This script should take a path to a directory as a command line argument. If one is
not provided or the argument is not a valid directory, you should print an error message and exit. Otherwise, your program
should print nothing.
In each directory in the inputted directory recursively, including the inputted directory itself, you should create a file named
index.json. If one is already present, you should overwrite it. No other files should be created, deleted, or modified.
index.json should be a JSON file that contains lists of the regular files and directories in that directory, and a relative
path back to the inputted directory. Your code should work correctly even if any filenames have spaces.
Directories may contain a file named _special and/or a file named _blacklist. Both of these files, if present, will have a
single filename on each line. If a file is in a directory’s _blacklist, it shouldn’t be included in that directory’s index.json.
If a file is in a directory’s _special, the file should go into a different section of that directory’s index.json. Neither the
_blacklist nor _special files themselves should be included in any index.json file lists.
index.json format
index.json should be a syntactically valid JSON file with an object containing the keys files, directories,
special_files, special_directories, and outer. Each key should have these values:
• files: A list of all regular files in the directory that aren’t in the directory’s _special file (if one exists) and aren’t
in the directory’s _blacklist file (if one exists), sorted alphabetically
• directories: A list of all directories in the directory that aren’t in the directory’s _special file (if one exists) and
aren’t in the directory’s _blacklist file (if one exists), sorted alphabetically
• special_files: A list of all regular files in the directory that are in the directory’s _special file (if one exists) and
aren’t in the directory’s _blacklist file (if one exists), sorted alphabetically
• special_directories: A list of all directories in the directory that are in the directory’s _special file (if one exists)
and aren’t in the directory’s _blacklist file (if one exists), sorted alphabetically
• outer: A relative path to the inputted directory
See here for more information about JSON (ignore the mentions of web development and JavaScript).
Example
Say we ran indexer on a directory named sample with this structure:
sample/
|-- bar
| |-- ...
|-- foo
| |-- baaz
| |-- _blacklist
| |-- _special
| |-- a_different_directory
| | |-- ...
| |-- abc
| | |-- ...
| |-- another file
| |-- file1
1
| |-- some_directory
| | |-- ...
| |-- this_file
| |-- x
| |-- y
| |-- yet another file
| |-- z
|-- ...
We’d create an index.json in sample, sample/bar, sample/foo, sample/foo/baaz, sample/foo/baaz/a_different_directoryetc. The index.json in sample/foo/baaz would have these contents
{
"files": ["another file", "file1", "this_file"],
"directories": ["some_directory"],
"special_files": ["x", "y", "z"],
"special_directories": ["a_different_directory"],
"outer": "../.."
}
if sample/foo/baaz/_special had these contents
x
a_different_directory
y
z
and sample/foo/baaz/_blacklist had these contents:
yet another file
abc
Tips
• You may find it helpful to use Bash arrays.
• You can check if a file is in valid JSON format by passing it to jq, a command line program that can parse and
pretty-print JSON, e.g. jq '.' my_json_file.json. Remember that, in JSON, whitespace doesn’t matter, all
strings must be double quoted, and arrays and objects can’t have trailing commas.
• We might call your program with a relative or an absolute path, or with a path ending with or without a trailing /,
which might affect how you compute how many .. to put in the relative path. Consider using realpath to normalize
paths and then removing the part of the path that’s in common with the outer directory, e.g. if the outer directory is
/home/nkl43/scratch/foo and you’re trying to compute the outer key for /home/nkl43/scratch/foo/bar/baaz’s
index.json, if you remove the outer directory part of baaz’s path, you get /bar/baaz, which we could then use to
compute how many .. to put in the outer value (in this case, ../..).
• Consider edge cases. What if a directory has no _blacklist and/or _special file? What if a directory has no
regular files and/or directories? What if the current directory is the outer directory itself (and what should outer be
in this case)? What if the outer directory has a space in its name?
Submit
Submit your indexer file to assignment assignment1 for grading.
2"""
candidate_labels = ["school", "work", "personal", "uncategorized"]

result = classifier(text, candidate_labels)

print(result)

# Get the highest-scoring category
highest_index = result['scores'].index(max(result['scores']))
highest_label = result['labels'][highest_index]

print(f"Highest category: {highest_label} with confidence {result['scores'][highest_index]:.2f}")

