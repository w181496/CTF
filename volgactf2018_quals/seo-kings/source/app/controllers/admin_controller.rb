require './app/controllers/application_controller.rb'





class AdminController < ApplicationController


 OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

  SECRET_TOKEN = "d595462f496fd347796b60b605b72ff6"

  get '/' do

    if local?
      token = params[:token]
      if(token == SECRET_TOKEN)
        @flag = Flagclass::FLAG
        erb :flag
      end
    else
        "Please, use local ip"
    end


  end
