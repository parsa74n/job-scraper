import quera
import jobinja
import linkedin
import jobvision
from concurrent.futures import ThreadPoolExecutor
import time
import argparse

sites={'quera':quera,
    'jobinja':jobinja,
    'jobvision':jobvision}


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False,description='''
    this a job scraper written in python. you can find your job title in quera, jobinja, jobvision if you are
    in iran. and if you are outside of iran and you want to find your job in linkedin you can do that.
    ''',epilog='''examples: 
    python main.py javascript -j quera -j jobvision --linkedin germany
    ''') 
    parser.add_argument('job_title',
                       type=str,
                       help='title of the job you are looking for')

    parser.add_argument('-j', action='append', choices=[job for job in sites.keys()],help='the web site you are looking for job in it')
    parser.add_argument('--linkedin',action='store',type=str,help='the location of company you are looking for in linkedin')
    args=parser.parse_args()

    job_title=args.job_title
    st=time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        if args.j:
            for i in args.j:
                executor.submit(sites.get(i).crawl,job_title)
        if args.linkedin:
            executor.submit(linkedin.crawl,job_title,args.linkedin)
    print(f'crawling duration :  {time.time()-st}')

if __name__=='__main__':
    main()
