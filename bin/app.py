import web
import os
from Plant import Plant
import sys

urls = (
  '/', 'Index',
  '/app', 'Labeling',
  '/print', 'Print',
  '/small_images/(.*)', 'images'
)

app = web.application(urls, globals())
#session = web.session.Session(app, web.session.DiskStore('sessions'),
#                              initializer={'user': None})

render = web.template.render('templates/', base="layout")

plant_code = ["CODE1","CODE2","CODE3","CODE4","CODE5"]

plants = Plant(7)

class Index(object):
    def GET(self):
        return render.login()

    #def POST(self):
        #form = web.input()
        #return render.labeling(password = form.pwd)
        #return render.index(word_to_print = form.pwd)


class Labeling(object):
    def GET(self):
        p = plants.next_plant(0)
        return render.labeling(user=None,plant_code=p[1],
                               image=p[0],num_plants=plants.N,
                               idx=p[3]+1)

    def POST(self):
        user = None
        form = web.input(user=None,selection=None,image=None,
                         img_index_dec=0,img_index_unit=0,changeimg=None,idx=0)

        if not form.user is None:
            user = form.user
        #    session.user = form.user
        if not form.selection is None:
            print form.image+'  '+form.selection
            plants.save_selection(form.image,form.selection)
        #if form.pwd == "biagio":

        if form.changeimg is None:
            p = plants.next_plant(int(form.idx))
        else:
            if form.changeimg=='change random':
                p = plants.next_plant(-1)
            else:
                p = plants.next_plant(int(form.img_index_dec)+int(form.img_index_unit)-1)

        return render.labeling(user=user,plant_code=p[1],
                               image=p[0],num_plants=plants.N,
                               idx=p[3]+1)
        #else:
        #    return render.login()

class Print(object):
    def GET(self):
        session.count += 1
        return render.printing()

    def POST(self):
        form = web.input(selection=None,user=None)
        return render.printing(to_print=session.user)

class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"small_images/png",
            "jpg":"small_images/jpeg",
            "gif":"small_images/gif",
            "ico":"small_images/x-icon"            }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('small_images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

if __name__ == "__main__":
    app.run()
