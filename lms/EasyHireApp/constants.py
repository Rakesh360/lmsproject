import datetime

current_year = datetime.datetime.now().date().year

YEAR_OF_PASSING = [year for year in range(current_year, current_year-40, -1)]

CONTENT_TYPE_JSON = "application/json"

NO_APPLICANT_PER_PAGE = 10
MAX_ACTIVE_ADMINISTRATOR = 10

CAMPUS = "1"
WALK_IN = "2"
POSTING = "3"

APPLICANT_CATEGORY = (
		(CAMPUS, "Campus"),
		(WALK_IN, "Walk-In"),
		(POSTING, "Posting"),
	)

APPLICANT_ROLE = "1"
ADMINISTRATOR_ROLE = "2"
OTHER_ROLE = "3"

USER_CHOICES = (
		(APPLICANT_ROLE,"Applicant"),
		(ADMINISTRATOR_ROLE,"Administrator"),
		(OTHER_ROLE, "Other")
)

APPLICANT_AT_QUIZ = "1"
APPLICANT_INTERVIEW = "2"

APPLICANT_APPLICATION_STATUS = (
		(APPLICANT_AT_QUIZ, "Quiz"),
		(APPLICANT_INTERVIEW, "Interview")
	)

APPLICANT_STATUS_DICT = {}
for key, value in APPLICANT_APPLICATION_STATUS:
	APPLICANT_STATUS_DICT[key]=value


# Quiz
DIFFICULTY_EASY = '1'
DIFFICULTY_MEDIUM = '2'
DIFFICULTY_HARD = '3'

DIFFICULTY_CHOICES = (
    (DIFFICULTY_EASY, 'Easy'),
    (DIFFICULTY_MEDIUM, 'Medium'),
    (DIFFICULTY_HARD, 'Hard'),
)

PROBLEM_CATEGORY_SINGLE_CORRECT = '1'
PROBLEM_CATEGORY_MULTI_CORRECT = '2'
PROBLEM_CATEGORY_DESCRIPTIVE = '3'
PROBLEM_CATEGORY_AUDIO = '4'
PROBLEM_CATEGORY_VIDEO = '5'

PROBLEM_CATEGORY_CHOICES = (
		(PROBLEM_CATEGORY_SINGLE_CORRECT,"Single Choice"),
		# (PROBLEM_CATEGORY_MULTI_CORRECT,"Multiple Choice"),
		# (PROBLEM_CATEGORY_DESCRIPTIVE,"Descriptive"),
		# (PROBLEM_CATEGORY_VIDEO,"Video"),
		# (PROBLEM_CATEGORY_AUDIO,"Audio")
	)

CATEGORY_MAPPING = {
	"SINGLE":PROBLEM_CATEGORY_SINGLE_CORRECT,
	"MULTIPLE":PROBLEM_CATEGORY_MULTI_CORRECT,
	"DESCRIPTIVE":PROBLEM_CATEGORY_DESCRIPTIVE,
	"AUDIO":PROBLEM_CATEGORY_AUDIO,
	"VIDEO":PROBLEM_CATEGORY_VIDEO
}

MALE = "1"
FEMALE = "2"
OTHERS = "3"
APPLICANT_GENDER = (
		(MALE, "Male"),
		(FEMALE, "Female"),
		(OTHERS, "Others"),
	)
BATCH_PROCESS_STARTING_HOURS = (
 	("0", "0"),
 	("1", "1"),
 	("2", "2"),
 	("3", "3"),
 	("4", "4"),
 	("5", "5"),
 	("6", "6"),
 	("7", "7"),
 	("8", "8"),
 	("9", "9"),
 	("10", "10"),
 	("11", "11"),
 	("12", "12"),
 	("13", "13"),
 	("14", "14"),
 	("15", "15"),
 	("16", "16"),
 	("17", "17"),
 	("18", "18"),
 	("19", "19"),
 	("20", "20"),
 	("21", "21"),
 	("22", "22"),
 	("23", "23"),
 )
BATCH_PROCESS_NUMBER_OF_HOURS = (
 	("1", "1"),
 	("2", "2"),
 	("3", "3"),
 	("4", "4"),
 	("5", "5"),
 	("6", "6"),
 	("7", "7"),
 	("8", "8"),
 	("9", "9"),
 	("10", "10"),
 	("11", "11"),
 	("12", "12"),
 	("13", "13"),
 	("14", "14"),
 	("15", "15"),
 	("16", "16"),
 	("17", "17"),
 	("18", "18"),
 	("19", "19"),
 	("20", "20"),
 	("21", "21"),
 	("22", "22"),
 	("23", "23"),
 )


TAG_CATEGORY_CHOICES = (
    ("1", "Quiz"),
    ("2", "Topic"),
    ("3", "Student"),
)
