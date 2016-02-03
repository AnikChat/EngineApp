#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# related third party imports
import webapp2

# local application/library specific imports
from Users import routes as routes_Users
from Images import routes as routes_Images
from Reports import routes as routes_Reports
from Users import config as config_Users



__author__ = 'Anik Chaturvedi (anik.chaturvedi@gmail.com)'
__website__ = 'www.UserImages.appspot.com'


webapp2_config = config_Users.config


app = webapp2.WSGIApplication([], debug=False, config=webapp2_config)

routes_Users.add_routes(app)
routes_Images.add_routes(app)
routes_Reports.add_routes(app)
