"""import sys
import project1

args_list = sys.argv
print(args_list)
redlist = []
data = []
namedata = ''
for i in range(len(args_list)):
    if (args_list[i] == '--input'):
        data = project1.readFiles(args_list[i + 1])
        i += 1
    elif (args_list[i] == '--names'):
        name_redacted, name_count = project1.redact_names(data)
        print(totaldata, name_count)
        redlist.append(args_list[i])
    elif (args_list[i] == '--dates'):
        date_redacted,date_count = project1.redact_dates(name_redacted)
        print(date_redacted)
        redlist.append(args_list[i])
    elif (args_list[i] == '--genders'):
        gender_redacted,gender_count= project1.redact_genders(date_redacted)
        print(gender_redacted)
        redlist.append(args_list[i])
    elif (args_list[i] == '--concept'):
        concept_redacted = project1.redact_concept(gender_redacted, args_list[i + 1])
        print(concept_redacted)
        i+=1
    elif (args_list[i] == '--output'):
        project1.write_output(concept_redacted,args_list[i+1])
        print()
        i+=1
    elif (args_list[i] == '--stats'):
        redlist = [str.strip('-') for str in redlist]
        statsdict = project1.stats(name_count,date_count,gender_count)
        project1.write_output(statsdict, redlist)
"""

import argparse
import project1

global final_data
if __name__=="__main__":
    parser =argparse.ArgumentParser()
    parser.add_argument("--input",type=str,required=True,action='append',help="It takes the patterns of the files")
    parser.add_argument("--output",type=str, required=True,help="It takes the output file path")
    parser.add_argument("--names",action="store_true",help="It helps in redacting names")
    parser.add_argument("--genders",action="store_true",help="It helps in redacting genders")
    parser.add_argument("--dates",action="store_true",help="It helps in redacting dates")
    parser.add_argument("--concept",type=str,required=True,help="It helps in redacting concepts")
    parser.add_argument("--stats",help="It provides the stats of the redacted flags")
    args=parser.parse_args()
    if args.input:
        final_data=project1.readFiles(args.input)
        #print(final_data)
    if args.names:
        final_data,names_count=project1.redact_names(final_data)
        #print(final_data)
    if args.dates:
        final_data,dates_count=project1.redact_dates(final_data)
        #print(final_data)
    if args.genders:
        final_data,gender_count=project1.redact_genders(final_data)
        #print(final_data)
    if args.concept:
        project1.redact_concept(final_data,args.concept)
    if args.stats:
        project1.stats(args.stats)
    if args.output:
        #print(final_data)
        project1.write_output(final_data,args.output)

