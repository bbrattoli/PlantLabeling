import numpy as np
import os

class Plant:

    def __init__(self, num_pred = 5,
                 epicode_path='./utils/eppocodes.txt',
                 prediction_path='./utils/predictions_website_2.npy',
                 manual_labels_path='./manual_labels/'):
        self.num_pred = num_pred
        self.epicodes = self.__read_epicodes__(epicode_path)
        self.predictions = self.__load_predictions(prediction_path)
        self.manual_labels_path = manual_labels_path
        self.N = len(self.predictions)
        print '----> Total images: %d <------'%self.N

    def __load_predictions(self,file_name):
        predictions = np.load(file_name)
        good_quality = self.__read_quality1_names()

        predictions_clean = []
        used = []
        deleted = []
        for i in range(predictions.shape[0]):
            if predictions[i]['image'] in good_quality:
                predictions_clean.append(predictions[i])
                used.append(predictions[i]['image'])
            else:
                deleted.append(predictions[i]['image'])

        predictions_clean = np.asarray(predictions_clean)

        out = open('used.txt','w')
        for name in used:
            out.write(name+'\n')
        out.close()

        out = open('deleted.txt','w')
        for name in deleted:
            out.write(name+'\n')
        out.close()

        return predictions_clean

    def next_plant(self,img_index=-1):
        N = len(self.predictions)
        if img_index==-1:
            i = np.random.randint(N)
        else:
            i = img_index
        plant = self.predictions[i]
        img = plant['image']

        codes, classes = self.__top_predictions__(plant['pred'])
        return img, codes, classes, i

    def save_selection(self,img,epicode):
        outfile = self.manual_labels_path+img+'.npy'
        if os.path.exists(outfile):
            tmp = np.load(outfile).tolist()
            tmp.append(epicode)
            np.save(outfile,tmp)
        else:
            np.save(outfile,[epicode])

        return

    def __top_predictions__(self,pred):
        I = pred.argsort()[::-1]

        classes = []
        codes = []
        for i in range(self.num_pred):
            idx = I[i]
            ec = self.epicodes[idx]
            codes.append([ec,int(pred[idx]*100)])
            classes.append(idx)

        return codes, classes

    def __read_epicodes__(self,path):
        f = open(path,'r')
        epicodes = f.readlines()
        epicodes2 = []
        for i in range(len(epicodes)):
            epicodes2.append(epicodes[i][0:-1])
        return epicodes2

    def __read_quality1_names(self):
        info = open('unlabeled_quality1.txt','r')
        rows = info.readlines()
        info.close()
        rows = [r[:-1] for r in rows]
        return rows


#outfile='/net/hciserver03/storage/bbrattol/webapp_py/plant_labeling/manual_labels/IR_1475750889304.jpg.npy'
def create_prediction_sample():
    os.chdir('/net/hciserver03/storage/bbrattol/webapp_py/plant_labeling/utils')
    images = os.listdir('../images/unlabeled_data/')

    predictions = []
    for i in range(len(images)):
        img = images[i]
        pred = np.random.rand(50)
        predictions.append({'image':img,'pred':pred})

    np.save('predictions.npy',predictions)

def test():
    plants = Plant('epicodes.txt','predictions.npy','../manual_labels/')
    plants.epicodes
    plants.predictions
    p = plants.next_plant()
    plants.save_selection(p[0],p[1][0],p[2][0])

#if __name__ == "__main__":
    #create_prediction_sample()
