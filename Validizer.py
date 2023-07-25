# Written by: Christopher Cormier
# Written on: 2023/06/24-2023/06/26
# Description: Validates common inputs and returns the input formatted to the correct standard in canada.

# Imports:
from datetime import *
import re

# Declaring variables
Month_Names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]
# Month names for date format.
Allowed_Characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-.' "
# You can add more if you expect clients/places with names that have characters not present here.
AcceptedCardTypes = {
    3: "Amex",
    4: "Visa",
    5: "MasterCard"
}
# Accepted card types and their names
CountryCode = "1"
# Country code you can change it here or simply pass it through when you use the phone_number validation.
LicencePlateFormat = "XXX 999"
PostalCodeFormat = "X9X-9X9"
PhoneFormat = "(999) 999-9999"
# Default formats for licence plate, postal code, and phone number. NL Canada.


# Processing functions:
# Checks if a number can be a float.
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# Checks if the day is valid for the specified year and day.
# Takes into account leap years.
def check_day_num(year):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 31, 31, 30, 31]
    if (year % 400 == 0) and (year % 100 == 0):
        month_days[1] = 29
    elif (year % 4 == 0) and (year % 100 != 0):
        month_days[1] = 29
    return month_days


# Fetches and returns a list of bank types for the bank type not accepted message.
def get_card_types():
    compiled = ""
    for i in AcceptedCardTypes:
        compiled = compiled + AcceptedCardTypes[i] + ", "
    return compiled[:len(compiled) - 2]


# Gets rid of symbols.
def strip(input_val, replace_character=""):
    return re.sub(r"[^\w]", replace_character, input_val).replace("_", replace_character)


# Validation class, contains all of the possible validations.
class Validate:
    # When defining a value through the Validate class like so: Value = Validate(Validate.type, "Input Prompt")
    # The class automatically loops the input for you and handles printing error messages,
    # it then assigns the input formatted to Value.V, raw input to Value.UP and type to Value.T
    # You can define your own function and pass it through here as long as it returns (Bool, Value) it'll work.
    def __init__(self, func, input_prompt: str, *args):
        if type(func) != str:
            pass
        elif type(func) == str:
            for i in dir(Validate):
                if i.lower() == func.lower():
                    func = getattr(Validate, i)
                    break
        else:
            print("Error: Validation set up incorrectly, function value must be string or function")
            print("Syntax: ValueName = Validate(Validate.function, *arguments)")
        while True:
            up_value = input(input_prompt)
            if len(args) == 0:
                error, value = func(up_value)
            else:
                error, value = func(up_value, *args)
            if not error:
                if isfloat(up_value) and func.__name__ == "number" and "$" in args:
                    self.NV = float(up_value)
                self.V = value
                self.UP = up_value
                self.T = func.__name__.replace("_", " ").title()
                break
            else:
                print(value)

    # Validates phone numbers, adjusts to follow standard format: +1 (999) 999-9999
    # You can also put in your own format
    @classmethod
    def phone_number(cls, input_val: str, phone_format=PhoneFormat, country_code=CountryCode) -> bool and str:
        error = False
        input_val = strip(input_val)
        length = len(strip(phone_format))
        if input_val.startswith(strip(country_code)) and len(input_val) > length:
            input_val = input_val[len(strip(country_code)):]
        if len(input_val) == length:
            for i, v in enumerate(phone_format):
                if v in "9":
                    if not input_val[i].isdigit():
                        error = True
                elif v in "X":
                    if not input_val[i].isalpha():
                        error = True
                else:
                    input_val = f"{input_val[:i]}{v}{input_val[i:]}"
            if error:
                input_val = f"Error: {input_val} does not follow format: {phone_format}"
                error = True
            else:
                input_val = f"+{country_code} {input_val}"
        else:
            input_val = f"Error: {input_val} is not {length} digits."
            error = True
        return error, input_val

    # Validates names, adjusts to title-case. By default uses Allowed_Characters set,
    # you may pass your own set through instead strings are converted to upper-case
    # when comparing to the set.
    @classmethod
    def name(cls, input_val: str, name_set=Allowed_Characters) -> bool and str:
        error = False
        if type(name_set) == set:
            char_set = name_set
        else:
            char_set = set(name_set.upper())
        if input_val.replace(" ", "") != "":
            if set(input_val.upper()).issubset(char_set):
                input_val = input_val.title()
            else:
                input_val = f"Error: {input_val} contains characters that are not allowed."
                error = True
        else:
            input_val = "Error: Name cannot be blank."
            error = True
        return error, input_val

    # Validates licence plate numbers, adjusts to upper-case.
    # Secondary value is  a custom format, must be done like so: XXXX 999
    # Will adjust input to match the format, 9 represents numbers X represents a letter.
    # Any symbols in the template are placed into the input string at the same position and returned.
    @classmethod
    def licence_plate(cls, input_val: str, lp_format=LicencePlateFormat) -> bool and str:
        error = False
        input_val = strip(input_val)
        length = len(strip(lp_format))
        if len(input_val) == length:
            for i, v in enumerate(lp_format):
                if v in "9":
                    if not input_val[i].isdigit():
                        error = True
                elif v in "X":
                    if not input_val[i].isalpha():
                        error = True
                else:
                    input_val = f"{input_val[:i]}{v}{input_val[i:]}"
            if error:
                input_val = f"Error: {input_val} does not follow format: {lp_format}"
            else:
                input_val = input_val.upper()
        else:
            error = True
            input_val = f"Error: {input_val} is not {length} digits."
        return error, input_val

    # Validates postal codes, adjusts to upper-case, takes in a template like licence plate validation.
    @classmethod
    def postal_code(cls, input_val: str, pc_format=PostalCodeFormat) -> bool and str:
        error = False
        input_val = strip(input_val)
        length = len(strip(pc_format))
        if len(input_val) == length:
            for i, v in enumerate(pc_format):
                if v in "9":
                    if not input_val[i].isdigit():
                        error = True
                elif v in "X":
                    if not input_val[i].isalpha():
                        error = True
                else:
                    input_val = f"{input_val[:i]}{v}{input_val[i:]}"
            if error:
                input_val = f"Error: {input_val} does not follow format: {pc_format}"
            else:
                input_val = input_val.upper()
        else:
            input_val = f"Error: {input_val} is not {length} digits."
            error = True
        return error, input_val

    # Validates numbers, returns input as either float or int, optional argument: range ("9-9")
    @classmethod
    def number(cls, input_val: str, return_type="Any", num_range=None) -> bool and int or float:
        error = False
        return_type = return_type.lower()
        if isfloat(input_val):
            if input_val.isdigit():
                input_val = int(input_val)
            else:
                input_val = float(input_val)
            if num_range and strip(num_range) != "":
                num_range_list = num_range.split("-")
                if isfloat(num_range_list[0]) and isfloat(num_range_list[1]):
                    if float(num_range_list[0]) <= input_val <= float(num_range_list[1]):
                        pass
                    else:
                        input_val = f"Error: {input_val} is not in range ({num_range_list[0]}-{num_range_list[1]})"
                        error = True
                else:
                    print(f"{num_range[0]} is not the correct format for range (9-9).")
            if return_type == "int":
                input_val = int(input_val)
            elif return_type == "float":
                input_val = float(input_val)
            elif return_type == "$":
                input_val = f"${input_val:,.2f}"
        else:
            if input_val.replace(" ", "") != "":
                input_val = f"Error: {input_val} is not a number."
            else:
                input_val = "Error: Value cannot be blank."
            error = True
        return error, input_val

    # Validates a range, returns a list with inputted numbers.
    @classmethod
    def range(cls, input_val: str, return_int=False) -> bool and list:
        error = False
        processed = strip(input_val, "-").split("-")
        if len(processed) == 2:
            if isfloat(processed[0]) and isfloat(processed[1]):
                processed[0], processed[1] = float(processed[0]), float(processed[1])
                if return_int:
                    processed[0], processed[1] = int(processed[0]), int(processed[1])
                if processed[0] <= processed[1]:
                    input_val = processed
                else:
                    input_val = f"Error: {processed[0]} is greater than: {processed[1]}"
                    error = True
            else:
                input_val = f"Error: {input_val} contains a non number character."
                error = True
        else:
            input_val = f"Error: {input_val} is not in correct format (9-9)."
            error = True
        return error, input_val

    # Validates MCP, adjusts to: 999 999 999 999
    @classmethod
    def mcp(cls, input_val: str) -> bool and str:
        error = False
        processed = strip(input_val)
        if processed.isdigit():
            if len(processed) == 12:
                input_val = processed[:3] + " " + processed[3:6] + " " + processed[6:9] + " " + processed[9:12]
            else:
                input_val = f"Error: {input_val} is not 12 characters."
                error = True
        else:
            input_val = f"Error: {input_val} is not a valid number."
            error = True
        return error, input_val

    # Validates bank card, takes into account AcceptedCardTypes, adjusts to: 9999-9999-9999-9999
    @classmethod
    def bank_card(cls, input_val: str) -> bool and str:
        error = False
        processed = strip(input_val)
        if processed.isdigit():
            if len(processed) == 16:
                input_val = processed[:4] + "-" + processed[4:8] + "-" + processed[8:12] + "-" + processed[12:16]
                if int(input_val[:1]) in AcceptedCardTypes:
                    pass
                else:
                    input_val = f"Error: {input_val} is not an accepted card type ({get_card_types()})."
                    error = True
            else:
                input_val = f"Error: {input_val} must be 16 digits."
                error = True
        else:
            input_val = f"Error: {input_val} is not a valid number."
            error = True
        return error, input_val

    # Validates strings, optional argument: Options ("X,X") adjusts input to fit option choice if valid.
    # (not case sensitive)
    # Adding a second option argument equal to True or False determines weather or not to match
    # user input to an option, i.e input = "ro" options = "Rock,Paper,Gun" match = True
    # output = Rock
    # Also returns error messages if there are too many or no matches. Adjusts options to
    # "Rock, Paper, Gun" for better looking output. Options must be separated with "," in a single string.
    @classmethod
    def string(cls, input_val: str, options="" or [], auto_complete=False) -> bool and str:
        error = False
        optionsvalid = False
        if input_val.replace(" ", "") != "":
            if type(options) is list:
                if len(options) > 0:
                    optionsvalid = True
            elif options.replace(" ", "") != "":
                optionsvalid = True
            if optionsvalid:
                if type(options) is not list:
                    split_opt = options.split(",")
                    words = []
                    word_comp = ""
                    for i in split_opt:
                        if " " in i:
                            word = i.split(" ")
                            for x in word:
                                if x.replace(" ", "") == "":
                                    word.remove(x)
                            if len(word) > 1:
                                comp = ""
                                for z in word:
                                    comp = comp + z + " "
                                word = comp[:len(comp)-1]
                            else:
                                word = word[0]
                        else:
                            word = i
                        words.append(word)
                        word_comp = word_comp + word + ", "
                    word_comp = word_comp[:len(word_comp)-2]
                elif type(options) is list:
                    word_comp = ""
                    words = options.copy()
                    for i in options:
                        word_comp = word_comp + i + ", "
                    word_comp = word_comp[:len(word_comp) - 2]
                else:
                    print("Error: Options type is invalid.")
                    return True, "Code Error: Options type is invalid."
                if auto_complete:
                    matches = []
                    for i in words:
                        if i.lower().startswith(input_val.lower()):
                            matches.append(i)
                    if len(matches) == 1:
                        input_val = matches[0]
                    elif len(matches) > 1:
                        input_val = f"Error: Too many matches for: {input_val}. Valid options: \n({word_comp})"
                        error = True
                    else:
                        input_val = f"Error: No matches for: {input_val}. Valid options: \n({word_comp})"
                        error = True
                else:
                    for i in words:
                        if i.lower() == input_val.lower():
                            input_val = i
                if input_val not in words and not error:
                    input_val = f"Error: {input_val} is not an option. Valid options: \n({word_comp})."
                    error = True
        else:
            input_val = "Error: Value cannot be blank."
            error = True
        return error, input_val

    # Validates dates, optional argument: Return Type: "string" returns a string formatted to YYYY-MM-DD, as opposed
    # to a datetime value which is the default.
    @classmethod
    def date(cls, input_val: str, return_type="datetime") -> bool and str or datetime:
        error = False
        input_val = strip(input_val, " ")
        processed = input_val.split(" ")
        if len(processed) == 3:
            if input_val.replace(" ", "").isdigit():
                if int(processed[1]) <= 12:
                    if int(processed[2]) <= check_day_num(int(processed[0]))[int(processed[1]) - 1]:
                        input_val = datetime.strptime(input_val, "%Y %m %d")
                        if return_type.lower() == "string":
                            input_val = datetime.strftime(input_val, "%Y-%m-%d")
                    else:
                        input_val = f"Error: {processed[2]} is not a valid day for: {Month_Names[int(processed[1])-1]}."
                        error = True
                else:
                    input_val = f"Error: {processed[1]} is not a valid month."
                    error = True
            else:
                input_val = f"Error: {input_val} contains a non-number character."
                error = True
        else:
            input_val = f"Error: {input_val} does not follow format (YYYY-MM-DD)"
            error = True
        return error, input_val



