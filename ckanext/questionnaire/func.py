from ckanext.questionnaire.model import Question
import ckan.model as model
from ckan.lib import base
import sqlalchemy as db


#Join the checkpoint answers function
def preprare_list(**in_dict):

    in_list = list(in_dict.items())
    out_list=[]

    i=0
    while i < len(in_list)-1:
        element1=str(in_list[i][0])
        element2=str(in_list[i][1])

        while element1[:6] == str(in_list[i+1][0][:6]) and i<len(in_list)-2:
            element2="<"+element2 +">"+"<" + str(in_list[i+1][1])+">"
            i=i+1
            
        out_list.append((element1, element2))
        i=i+1
    #the last element check
    if str(in_list[len(in_list)-1])[:6] == str(in_list [len(in_list)-2])[:6]:
        out_len=(len(out_list))
        element1=str(out_list[out_len-1][0])
        element2="<" + str(out_list[out_len-1][1]) + ">" + "<" + str(in_list[len(in_list)-1][1])+">"
        out_list[out_len-1]=((element1, element2))
    else:
        out_len=(len(out_list))
        in_len=len(in_list)
        out_list.append(in_list[in_len-1])
        #breakpoint()
    
    return (out_list)

#Get checkpoint Questions by ID function

def q_text(*in_list):
    
    y=[]
    for i in in_list:
        if i[0][:4] == "00qu":
            qid = i[0][-36:]
            q_text= model.Session.query(Question).filter(Question.id == qid).first().question_text
            y.append((q_text, i[1]))
        else:
            y.append(i)

    return(y)


