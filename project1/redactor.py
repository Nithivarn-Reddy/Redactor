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

