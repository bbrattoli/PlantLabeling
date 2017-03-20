import web
import os
from Plant import Plant

urls = (
  '/', 'Index',
  '/app', 'Labeling',
  '/print', 'Print',
  '/images/(.*)', 'images'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

plant_code = ["CODE1","CODE2","CODE3","CODE4","CODE5"]

plants = Plant()


class Index(object):
    def GET(self):
        return render.login()

    #def POST(self):
        #form = web.input()
        #return render.labeling(password = form.pwd)
        #return render.index(word_to_print = form.pwd)


class Labeling(object):
    def GET(self):
        return render.labeling()

    def POST(self):
        form = web.input(pwd="no_pwd",selection=None,image=None)
        if not form.selection is None:
            print form.image+'  '+form.selection
            plants.save_selection(form.image,form.selection)
        #if form.pwd == "biagio":
        p = plants.next_plant()
        return render.labeling(plant_code=p[1],image=p[0])
        #else:
        #    return render.login()

class Print(object):
    def GET(self):
        return render.printing()

    def POST(self):
        form = web.input(selection="NONE")
        return render.printing(to_print=form.selection)

class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"            }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

if __name__ == "__main__":
    app.run()
