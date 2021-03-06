import warnings
warnings.filterwarnings(action='ignore')
from tqdm import tqdm
import pandas as pd
import seaborn as sns
sns.set_style("whitegrid")
pd.set_option('display.max_columns', None )
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None )
import pickle
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt



##############################################
####################### MERGE DATA
##############################################

def merge_data(x):
    d = pd.DataFrame(  columns=['page', 'date', 'tags', 'questions', 'questions_add', 'answers', 'N_answer', 'url', 'category'])

    for i, j in zip( ['2020','2020','2020','2020','2020','2020','2020',
                      '2021','2021','2021','2021','2021','2021','2021','2021'],
                     ['06', '07', '08', '09', '10', '11', '12',
                      '01', '02', '03', '04', '05', '06', '07'] )  :

        df = pd.read_csv('/Users/janechoi/PycharmProjects/vaccine/final/['+str(i)+'.'+str(j)+']crawling.csv')
        print('/Users/janechoi/PycharmProjects/vaccine/final/['+str(i)+'.'+str(j)+']crawling.csv', df.shape)
        d = pd.concat([d, df], axis=0)
        d = d.drop_duplicates(['date', 'questions', 'questions_add','answers'])
        print('total data shape is ', d.shape)

    d.to_csv('/Users/janechoi/PycharmProjects/vaccine/final/final_data.csv',index=False)
    # with open("0824_naver_org_data", "wb") as file:
    #     pickle.dump(d, file)

##############################################
####################### PREPROCESS DATASET (INCLUDE/EXCLUDE WORDS)
##############################################

def pre_process():
    data =pd.read_csv('/Users/janechoi/PycharmProjects/vaccine/final/final_data.csv')

    data = data.sort_values('date')
    data['date']  = pd.to_datetime(data['date'])
    data = data[data['date'] >= '2020-06-27']
    data = data[data['date'] <= '2021-06-27']
    data.reset_index(inplace = True , drop = True )
    print(data.shape) #(60130, 9)
    vaccine_words = 'pcr(?i)(?:\s)*(??????)*|?????????(?:\s)*??????|vaccine(?i)|coronavac(?i)|astrazeneca(?i)|moderna(?i)|pfizer(?i)|????????????|??????(???|???)|(?:\s|^)??????(?:\s|\-)*??????(?:\s)*???(?:\s|$)|(?:\s|^)??????(?:\s|\-)*??????(??????|???)(?:\s|$)|(?:\s|^)(C|c)(O|o)(V|v)(I|i)(d|D)(?:\s|\-)*(19)*(?:\s|$)|(?:\s|^)(C|c)(O|o)(R|r)(o|O)(n|N)(A|a)(?:\s|\-)*(19)*(?:\s|$)|(?:\s|^)(?????????|?????????)(?:\s|\-)*(19)*(?:\s|$)|???????????????(???|???)???|??????|?????????|?????????|(A|a)(Z|z)|(?:\s|^)??????(?:\s)*??????(?:\s|$)|(?:\s|^)(??????)*(?:\s)*??????(?:\s|$)|(?:\s|^)10(?:\s)*??????(?:\s|$)|??????|??????|?????????'
    stop_words = '?????????|??????|??????(?:\s)*??????|\#????????????|??????(?:\s)*??????|(??????|???|?????????|??????|??????)(?:\s)*???|??????|??????(?:\s)*??????|(??????)*(?:\s)*(??????|??????)|????????????|(?????????|(P|p)(y|Y)(T|t)(h|H)(o|O)(n|N))|(?:\s|^)(???????????????)*(?:\s)*?????????(?:\s|$)|(?:\s|^)??????(?:\s)*(??????)*(?:\s|$)|(?:\s|^)(??????)*(?:\s)*??????(?:\s|$)|(?:\s|^)???(???|???)(?:\s|$)|(?:\s|^)?????????(?:\s)*(??????)*(?:\s|$)|(?:\s|^)???(?:\s)*(??????)*(?:\s|$)|(?:\s|^)(??????)*(?:\s)*??????(?:\s|$)|??????|????????????|(?:\s|^)(h|H)(p|P)(V|v)(?:\s|$)|(?????????|?????????)|(?:\s|^)??????(?:\s)*(??????)*(?:\s|$)|?????????|(?:\s|^)???(???)*???(?:\s|$)|?????????|(?:\s|^)???(???|???)(?:\s|$)|????????????|?????????|(?:\s|^)???(???|??????)(?:\s|$)|????????????'
    cat = ['questions_add','questions', 'answers']
    for c in cat:    data.loc[data[c].str.contains(vaccine_words, regex=True, na = False), 'INCLUDE'] =True
    print(data[data['INCLUDE']==True].shape)  #(35751, 10)
    for c in cat:  data.loc[data[c].str.contains(stop_words, regex=True, na=False), 'INCLUDE'] = False
    print(data[data['INCLUDE']==True])
    data= data[data['INCLUDE']==True]
    data = data.fillna('')
    print(data.head(50))
    print(data.tail(50))
    print(data.shape) #26987
    data.to_csv('preprocess_naver_data.csv', index=False )
    with open( "0825_naver_preprocessed_data", "wb" ) as file: pickle.dump(data, file)

##############################################
####################### SIMPLE EDA PURPOSE
##############################################

def eda():
    with open( "0825_naver_preprocessed_data", "rb" ) as file: data = pickle.load(file)
    print(data)
    print(data['url'][:20])

    # 1. Boxplot n_answer
    # sns.boxplot(y= 'N_answer',   data= data)
    # plt.title('[NAVER] Stats for total number of answer')
    # plt.savefig('box_n_answer_naver.png',dpi =300)
    # plt.show()

    # 2. scatter_n_answer
    # sns.scatterplot(y= 'N_answer', x='date' , data= data,s=15, alpha = 0.5 )
    # plt.title('[NAVER] Total number of answers')
    # plt.savefig('scatter_n_answer_naver.png',dpi =300)
    # plt.tight_layout()
    # plt.show()

    # 3. mean of n_answer by 2weeks
    # data.set_index('date', inplace=True)
    # df = pd.DataFrame(data.N_answer.resample('2W').mean())
    # df.columns = ['Mean_N_answer']
    # print(df)
    # sns.lineplot(x = 'date', y = 'Mean_N_answer', data= df)
    # plt.axvline(pd.to_datetime('2021-02-26') ,color= 'red')
    # plt.savefig('mean_of_a_2k_naver.png',dpi =300)
    # plt.tight_layout()
    # plt.show()



    # 4. median of n_answer by 2weeks
    # data.set_index('date', inplace=True)
    # df = pd.DataFrame(data.N_answer.resample('2W').median())
    # df.columns = ['Median_N_answer']
    # print(df)
    # sns.lineplot(x = 'date', y = 'Median_N_answer', data= df)
    # plt.axvline(pd.to_datetime('2021-02-26') ,color= 'red')
    # plt.savefig('median_of_a_2k_naver.png',dpi =300)
    # plt.tight_layout()
    # plt.show()



    # 5. n of questions by 2weeks
    # df = pd.DataFrame(data.groupby('date')['questions'].nunique())
    # df.columns =['n_questions']
    #
    # df = pd.DataFrame(df.n_questions.resample('2W').sum())
    # df.columns = ['Sum_n_questions']
    # print(df)
    # sns.lineplot(x = 'date', y = 'Sum_n_questions', data= df)
    # plt.axvline(pd.to_datetime('2021-02-26') ,color= 'red')
    # plt.savefig('n_of_q_2k_naver.png',dpi =300)
    # plt.tight_layout()
    # plt.show()


##############################################
####################### KOREAN WORDS FREQ CHECK
##############################################

def korean_words_frequency(data):
    q = ''.join(data['questions'])
    r = ''.join(data['questions_add'])
    l = ''.join(data['answers'])
    d = q+r+l
    def count_okt(t):
        okt = Okt() #twitter
        noun = okt.nouns(t)
        c = Counter(noun)
        for i,v  in c.most_common(50) :
            if len(i) >=  2  :  print(i,v)


    print(' ')
    print('questions')
    count_okt(q)

    print(' ')
    print('questions add')
    count_okt(r)

    print(' ')
    print('answers')
    count_okt(l)

    print('all together ')
    count_okt(d)



if __name__ == "__main__":
    # merge_data(x)
    # pre_process()
    eda() # 26987,10


