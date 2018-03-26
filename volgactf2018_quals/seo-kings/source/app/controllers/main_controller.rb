require './app/controllers/application_controller.rb'

require 'timeout'


class MainController < ApplicationController


 OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

  get '/' do

    erb :main
  end

   post '/' do
    site = params[:site]
    unless site.nil?
      runAdmin(site)
    end
    erb :main
  end


  get '/validator' do
    unless local?
      "Please, use local ip"
    else
      @site = params[:site]
      erb :validator
    end

  end

   get '/*' do
    erb :page_error
  end


  def runAdmin(site)
  pid = Process.spawn("phantomjs --web-security=no bot.js '" +  URI.escape(site)  + "'")
  begin
      Timeout.timeout(1) do
      Process.wait(pid)
    end
  rescue Timeout::Error
      Process.kill('TERM', pid)
  end

  end

  def local?
    request.ip == "127.0.0.1"
  end
