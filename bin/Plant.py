import numpy as np
import os

class Plant:

    def __init__(self,
                 epicode_path='./utils/epicodes.txt',
                 prediction_path='./utils/predictions_website.npy',
                 manual_labels_path='./manual_labels/'):
        self.epicodes = self.__read_epicodes__(epicode_path)
        self.predictions = np.load(prediction_path)
        self.manual_labels_path = manual_labels_path

    def next_plant(self):
        N = len(self.predictions)
        i = np.random.randint(N)
        plant = self.predictions[i]
        img = plant['image']

        codes, classes = self.__top_predictions__(plant['pred'])
        return img, codes, classes

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
        for i in range(5):
            idx = I[i]
            ec = self.epicodes[idx]
            codes.append(ec)
            classes.append(idx)

        return codes, classes

    def __read_epicodes__(self,path):
        f = open(path,'r')
        epicodes = f.readlines()
        epicodes2 = []
        for i in range(len(epicodes)):
            epicodes2.append(epicodes[i][0:-1])
        return epicodes2

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