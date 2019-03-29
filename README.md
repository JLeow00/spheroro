# spheroro
Django backend for sphero control

Sphero Edu App: [Windows store](https://www.microsoft.com/en-us/p/sphero-edu/9n2796r62xlz?activetab=pivot:overviewtab)

Sphero Node.js SDK: https://www.npmjs.com/package/sphero and https://github.com/orbotix/sphero.js

## Tests done on Sphero:
- Controlling sphero with Django server on localhost outside sphero edu app (Done)
- Controlling multiple spheros with same computer (Not possible with sphero edu, unknown if possible with Node.js SDK)

## Controlling sphero with external server
Able to control sphero from outside the sphero edu app. Django server is in the file 'sphero', the app that controlls the ball is in `/spheroproject`, and the app is in `localhost:8000/ball` if you run server with the default settings, because of this code in `/sphero/urls.py`

```python
urlpatterns = [
	path('ball/', include('spheroproject.urls')),
  path('admin/', admin.site.urls),
]
```

The intended direction of the ball is saved in the Django model `Direction`, which takes in a string that is either `'up'`, `'down'`, '`left'`, or `'right'`. 

On loading `/spheroproject`, the current `Direction` from the database will be read and returned directly as a `HTTPResponse`. See `/spheroproject/views.py`:
```Python
def index(request):
	directions = Direction.objects.all()
	for direction in directions:
		return HttpResponse(direction.direction)
```

To change the direction of the sphero, go to `localhost:8000/ball/change`, and 4 links with the 4 directions will show, html rendered from `/spheroproject/templates/spheroproject/change.html`. Clicking on any link will redirect to `/ball/changedirection/direction`, which would capture the direction and update the database, before redirecting back to `localhost:8000/ball/change`. See `spheroproject/views.py`
```python
def changedirection(request, dir):
	Direction.objects.all().update(direction=dir)
	return HttpResponseRedirect("/ball/change/")
```

The JS code that is run from sphero edu checks `localhost:8000/ball` every 3 seconds to get the direction set, then moves in that direction. See below.

```js
async function startProgram() {
 // Write code here
 setInterval(move, 3000);

}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

async function move(){
 switch (httpGet('http://localhost:8000/ball/')) {
  case "up":
   await roll(0, 100, 1);
   break;
   
  case "down":
   await roll(180, 100, 1);
   break;
   
  case "left":
   await roll(270, 100, 1);
   break;
   
  case "right":
   await roll(90, 100, 1);
   break;
 }
}
```
As can be seen, 'up', 'down', 'left' and 'right' just correspond to rolling 0, 180, 270 and 90 degrees respectively. Thus we can easily change the Django model `Direction` to be an integer between 0 and 360 and just get the sphero to `await roll()` with the exact direction which would be much more useful that having just 4 directions to work with.

One way to make the sphero move once instead of moving every 3 seconds is to change the direction to a 'halt' command everytime a get request is made, setting `direction = -1` for example.
