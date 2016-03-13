<img src="./QuesCheetah/static/images/qc_logo.png" width="100"><img src="./QuesCheetah/static/images/quescheetah-logo.png" width="400">


---
# QuesCheetah

Web Platform with Django for the fast/easy Q&A of your site. Go check our [homepage](quescheetah.com).

*Receiving realtime data through socket server is not completed yet. But you can install it and manipultate coming data.*

* Supports REST API request realated with question data.
* Provides dashboard page to manage results.
* Can be install easily with bundle js file fot [sample widget](https://github.com/mingkim/QuesCheetah_sample).
* Supports realtime data feature with our [socket server](https://github.com/mingkim/QuesCheetah-socket). 

## Document / Tutorial
---
* [Overview]()
* [JavaScript SDK](https://mingkim.gitbooks.io/quescheetah-tutorial/content/js-SDK.html)
* [REST API](https://mingkim.gitbooks.io/quescheetah-document/content/)
* [Install with Jekyll](https://mingkim.gitbooks.io/quescheetah-tutorial/content/jekyll.html)
* [Customizing sample widget](https://mingkim.gitbooks.io/quescheetah-tutorial/content/customize-sample.html)
 

## Basic Use of sample widget
---
To use sample widget, import [jQuery](http://jquery.com/) and [Bootstrap](http://getbootstrap.com/) first.

```html
<!DOCTYPE html>
<html lang="en-us">
  <head>
    <title>My Blog</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
  </head>
  <body>
    <!-- widget will be displayed -->
  </body>
  <script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</html>
```

Make a new div as follows inside body tag. "gid" property means id of created group question.
```html
<div id="systemjs-sample" gid="5"></div>
```

Insert our bundle js file  under the bootstrap file. This file includes JavaScript SDK, html, css, js files to start widget. 
```html
<script src="js/bundle-0.0.1.js"></script>
```

In the code of SDK file, replace "your-api-key" value inside the "config" object.

```javascript
$__System.register('7', ['10'], function (_export) {
    'use strict';

    var config, qc;
    return {
        setters: [function (_) {}],
        execute: function () {
            config = {
                'apiKey': 'your-api-key',
                'callBackUrl': 'http://localhost:8000',
                'receiveRealtimeResponse': false
            };
            qc = new QuesCheetah(config);

            _export('qc', qc);
        }
    };
});
```

After refresh the page, our simple widget will show.
![image](http://i67.tinypic.com/98g1md.png)

## Running the test
---
You can use our .yml files for using CircleCI, TravisCI. Or just enter this command in project directory.
```python
./manage.py test
```

## License
---
MIT

