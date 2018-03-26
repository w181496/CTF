Dir["./app/constants/*.rb"].each {|file| require file }
class ApplicationController < Sinatra::Base

  set :views, File.expand_path('../../views', __FILE__)
  set :public_folder, File.expand_path('../../public', __FILE__)


  configure :production do
    enable :logging
  end

 def local?
    request.ip == "127.0.0.1"
 end
