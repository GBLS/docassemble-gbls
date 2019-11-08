
/**
*
*  Base64 encode / decode
*  http://www.webtoolkit.info
*
**/
var Base64 = {

    // private property
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    // public method for encoding
    , encode: function (input)
    {
        var output = "";
        var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
        var i = 0;

        input = Base64._utf8_encode(input);

        while (i < input.length)
        {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);

            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;

            if (isNaN(chr2))
            {
                enc3 = enc4 = 64;
            }
            else if (isNaN(chr3))
            {
                enc4 = 64;
            }

            output = output +
                this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) +
                this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);
        } // Whend 

        return output;
    } // End Function encode 


    // public method for decoding
    ,decode: function (input)
    {
        var output = "";
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;

        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        while (i < input.length)
        {
            enc1 = this._keyStr.indexOf(input.charAt(i++));
            enc2 = this._keyStr.indexOf(input.charAt(i++));
            enc3 = this._keyStr.indexOf(input.charAt(i++));
            enc4 = this._keyStr.indexOf(input.charAt(i++));

            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;

            output = output + String.fromCharCode(chr1);

            if (enc3 != 64)
            {
                output = output + String.fromCharCode(chr2);
            }

            if (enc4 != 64)
            {
                output = output + String.fromCharCode(chr3);
            }

        } // Whend 

        output = Base64._utf8_decode(output);

        return output;
    } // End Function decode 


    // private method for UTF-8 encoding
    ,_utf8_encode: function (string)
    {
        var utftext = "";
        string = string.replace(/\r\n/g, "\n");

        for (var n = 0; n < string.length; n++)
        {
            var c = string.charCodeAt(n);

            if (c < 128)
            {
                utftext += String.fromCharCode(c);
            }
            else if ((c > 127) && (c < 2048))
            {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else
            {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }

        } // Next n 

        return utftext;
    } // End Function _utf8_encode 

    // private method for UTF-8 decoding
    ,_utf8_decode: function (utftext)
    {
        var string = "";
        var i = 0;
        var c, c1, c2, c3;
        c = c1 = c2 = 0;

        while (i < utftext.length)
        {
            c = utftext.charCodeAt(i);

            if (c < 128)
            {
                string += String.fromCharCode(c);
                i++;
            }
            else if ((c > 191) && (c < 224))
            {
                c2 = utftext.charCodeAt(i + 1);
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                i += 2;
            }
            else
            {
                c2 = utftext.charCodeAt(i + 1);
                c3 = utftext.charCodeAt(i + 2);
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                i += 3;
            }

        } // Whend 

        return string;
    } // End Function _utf8_decode 

}

  /**
   * Strip out bad characters so that we can place legal server fields in the GET query
   * @param {*} valueText - HTML element representing Legal Server field
   */
  function fixValue(valueText) {
    var theValue;
    valueText = valueText.replace(/<br ?\/?>/g, "\n").replace(/\<[^\>]+\>/g, '').replace(/(^ +| +$)/g, '').replace(
      /  +/g, ' ').replace(/ ?\[Edit\]/g, '').replace(/ *\n+ */g, ", ");
    if (valueText == 'Yes')
      theValue = true;
    else if (valueText == 'No')
      theValue = false;
    else if (valueText == 'N/A' || valueText == '')
      theValue = null;
    else
      theValue = valueText;
    return theValue;
  }

  function getCleanArgs() {
    var args = {
      id: jQuery("header.Main ul li h2").html().replace(/^.*\(/, '').replace(/\)$/, ''),
      name: jQuery("header.Main hgroup h1").html(),
      initiating_user: jQuery("li.user a strong").html(),
      initiating_user_email_address: jQuery('input[name="bug_sender_email"]').val(),
      sidebar_domestic_violence: null,
      sidebar_unsafe_address: null
    };
    jQuery("#sidebar table tr").each(function () {
      if (jQuery(this).find("td").length > 0) {
        var labelText = 'sidebar_' + jQuery(this).find("th").text().toLowerCase().replace(/[^a-z]+/g, '_').replace(
          /(^_|_$)/g, '');
        if (labelText == 'sidebar_' && jQuery(this).find("th").next().length) {
          var theMessage = jQuery(this).find("th").next().html();
          if (theMessage == 'Address Not Safe') {
            args['sidebar_unsafe_address'] = true;
          }
        }
        if (labelText != 'sidebar_') {
          var valueText = jQuery(this).find("th").next().html();
          if (labelText == 'sidebar_disposition_case_status_date_open') {
            var theVals = fixValue(valueText).split(", ");
            args['sidebar_disposition'] = theVals[0];
            args['sidebar_case_status'] = theVals[1];
            args['sidebar_date_open'] = theVals[2];
          } else {
            args[labelText] = fixValue(valueText);
          }
        }
      } else {
        var valueText = jQuery(this).find("th").text();
        if (valueText.indexOf('@') > -1) {
          args['case_email'] = valueText;
        }
      }
    });
    jQuery("td.form_label label").each(function () {
      if (jQuery(this).attr('for')) {
        var elem = document.getElementById(jQuery(this).attr('for'));
        if (elem.tagName != 'SELECT' && elem.tagName != 'INPUT') {
          var labelText = jQuery(this).text().toLowerCase().replace(/[^a-z]+/g, '_').replace(/(^_|_$)/g, '');
          var valueText = jQuery(elem).html(); //.replace(/ *\[Edit\]/, '');
          args[labelText] = fixValue(valueText);
        }
      }
    });
    if (args['address']) {
      if (args['address'].startsWith("(Safe)")) {
        args['safe_address'] = true;
      } else if (args['address'].startsWith("(Not Safe)")) {
        args['safe_address'] = false;
      }
      args['address'] = args['address'].replace(/^\((Safe|Not Safe)\) */, '');
    }

    //console.log(args)

    var containers = document.getElementsByClassName('form_container');
    //var all_tables = {}
    for (var i = 0; i<containers.length; i++) {
      var datatables = containers[i].getElementsByClassName('datatable');
      var section_heads = containers[i].getElementsByClassName('form_section');
      tables_match_labels = datatables.length == section_heads.length
      if (!tables_match_labels) {
        //console.log('Not all listviews in this section are labeled. Display the label to add listview name to url_args.');
      }
      for (var j=0; j<datatables.length; j++) {
        label = tables_match_labels ? section_heads[j].innerText : datatables[j].id

        var cols = datatables[j].getElementsByTagName('th');
        var body = datatables[j].getElementsByTagName('tbody')[2]; // contains content
        if (body) {
          var table = Array();
          rows = body.getElementsByTagName('tr');
          for (var k=0;k<rows.length; k++) {
            var new_row = {}
            var cells = rows[k].getElementsByTagName('td');
            for (var l=0;l<cells.length; l++) {
              new_row[cols[l].textContent] = cells[l].textContent;
            }
            table.push(new_row);
          }
          args[label] = table;
        }
      }
    }
    
    return args
  }

  function loadInterviews(divTitle, variableJSON, tags = [], useEveryoneTag = true) {
    var request = new XMLHttpRequest();
    var mydiv = document.getElementById(divTitle);
    document.getElementById('docassemble_container').parentElement.setAttribute('class','book');

    da_api_url = document.getElementById('da_api_url').value;
    da_api_key = document.getElementById('da_api_key').value;
    da_request_url = da_api_url + da_api_key;

    console.log(da_request_url);

    request.open('GET', da_request_url , true);
    request.onload = function () {
      // Begin accessing JSON data here
      var data = JSON.parse(this.response);
      var table = document.createElement('table');      
      table.setAttribute('class',"tablelistview");
      table.innerHTML = "<thead><th class='tablehead'>Interview Link</th><th class='tablehead'>Tags</th></thead>";
      tbody = document.createElement('tbody');
      var loop=1
      if (useEveryoneTag) {
        tags.push('everyone') // By default, always check for interviews tagged "everyone"
      }
      for (var interview of data) {
        if (tags.length < 1 || (tags.filter(value => interview['tags'].includes(value))).length > 0) {
          var row = tbody.insertRow(0);
          row_class = loop % 2 == 0 ? "listviewRowEven" : "listviewRowOdd";
          row.setAttribute('class', row_class)
          var cell = row.insertCell(0);
          //mydiv.appendChild(li);
          var aTag = document.createElement('a');
          aTag.setAttribute('href', interview['link'] + '&args=' + variableJSON+'&new_session=1');
          aTag.innerHTML = interview['title'];
          aTag.target = "_blank";
          cell.appendChild(aTag);
          var tag_cell = row.insertCell();
          tag_cell.innerHTML = interview['tags'].join();
          //console.log(interview['link']);
          loop++;
        }
      }
      table.appendChild(tbody);
      mydiv.appendChild(table)
    }

    request.send();
  }

  function myOnLoad(event) {
    document.getElementById('docassemble-fields').parentElement.parentElement.style.display = 'none'
    var theValues = getCleanArgs()
    //theValues['sidebar_assignment_program']
    loadInterviews("interviews",  encodeURIComponent(Base64.encode(JSON.stringify(theValues))), [theValues['sidebar_assignment_program']]);
  }

  if (window.attachEvent) {
    window.attachEvent('onload', myOnLoad);
  } else {
    if (window.onload) {
      var curronload = window.onload;
      var newonload = function (evt) {
        curronload(evt);
        myOnLoad(evt);
      };
      window.onload = newonload;
    } else {
      window.onload = myOnLoad;
    }
  }
