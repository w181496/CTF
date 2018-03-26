require 'sinatra'
require "open-uri"
require 'openssl'
require 'uri'

require 'sinatra/base'


Dir.glob('./app/{controllers}/*.rb').each { |file| require file }


map('/') { run MainController }
map('/admin') { run AdminController}
