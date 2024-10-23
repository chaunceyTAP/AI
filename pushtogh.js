loadLibrary('xtk:common.js')
loadLibrary('xtk:shared/json2.js')

function getBranches() {
  var req = new HttpClientRequest(
    'https://api.github.com/repos/TAP-CXM/TAPSandbox/git/refs/heads/main'
  )

  req.method = 'GET'

  req.header['User-Agent'] = 'chaunceyTAP'
  req.header['Accept'] = 'application/vnd.github+json'
  req.header['Content-Type'] = 'application/json'
  req.header['X-GitHub-Api-Version'] = '2022-11-28'
  req.header['X-OAuth-Scopes'] = 'repo, user'
  req.header['X-Accepted-OAuth-Scopes'] = 'repo'
  req.header['Authorization'] =
    'Bearer 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'

  req.execute()

  var response = req.response

  var body = response.body
  // logInfo(typeof(body));
  var bodyAsJson = JSON.parse(body)

  var baseTreeSha = bodyAsJson.object.sha

  //logInfo(baseTreeSha);

  function viewCommit(baseTreeSha) {
    var URL =
      'https://api.github.com/repos/TAP-CXM/TAPSandbox/git/commits/' +
      baseTreeSha
    var req = new HttpClientRequest(URL)

    req.method = 'GET'

    req.header['User-Agent'] = 'chaunceyTAP'
    req.header['Accept'] = 'application/vnd.github+json'
    req.header['Content-Type'] = 'application/json'
    req.header['X-GitHub-Api-Version'] = '2022-11-28'
    req.header['X-OAuth-Scopes'] = 'repo, user'
    req.header['X-Accepted-OAuth-Scopes'] = 'repo'
    req.header['Authorization'] =
      'Bearer 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'

    req.execute()

    var response = req.response

    var body = response.body
    var bodyAsJson = JSON.parse(body)

    var treeSha = bodyAsJson.tree.sha

    //document.write(treeSha);
    //logInfo("THis is the base tree:  " + baseTreeSha);
    //logInfo("This is the commit tree :  " + treeSha);
    function createTree(baseTreeSha, treeSha) {
      /*   
                                      
                                      function parseXmlToJson(xml) {
                                                  const json = {};
                                                for (const res of xml.matchAll((?:<(\w*)(?:\s[^>]*)*>)((?:(?!<\1).)*)(?:<\/\1>)|<(\w*)(?:\s*)*\/>) {
                                                    const key = res[1] || res[3];
                                                    const value = res[2] && parseXmlToJson(res[2]);
                                                    json[key] = ((value && Object.keys(value).length) ? value : res[2]) || null;
                                            
                                                }
                                                return json;
                                              }
            */
      function getData() {
        var query = xtk.queryDef.create(
          <queryDef schema='xtk:specFile' operation='select'>
            <select>
              <node expr='@label' />
              <node expr='data' />
              <node expr='@name' />
              <node expr='@namespace' />
            </select>
            <where>
              <condition expr="Lower(@name)= 'auditdashboardv1'" />
            </where>
          </queryDef>
        )
        var result = query.ExecuteQuery()

        var resultString = result.toXMLString()
        var domDoc = DOMDocument.fromXMLString(resultString)
        var label = domDoc.root.getValue('/specFile/@name')
        //var validLabel = label.getAttribute('label');
        //logInfo(typeof(label));
        logInfo(label)

        var res = domDoc.toXMLString(true)
        //var resJson = res.toXMLString();

        //logInfo(typeof(res));
        var info = [label, res]

        //var newResult = result['@name'].toXMLString();
        //logInfo(result);
        //return result;
        return info
      }

      var newResult = getData()
      // var label = newResult['specFile-collection']['specFile']
      //logInfo(newResult.$data);

      // var json = parseXmlToJson(newResult)
      //logInfo(newResult);
      // var content = newResult['specFile'];

      // var string = newResult.toXMLString();
      //var data = newResult['specFile'].toXMLString();
      //logInfo("data is a " + typeof(data));
      var URL = 'https://api.github.com/repos/TAP-CXM/TAPSandbox/git/trees'
      var req = new HttpClientRequest(URL)
      //var label = newResult['specFile'].@name.toXMLString();

      //logInfo('this is the new result' + string);
      req.method = 'POST'

      req.header['User-Agent'] = 'chaunceyTAP'
      req.header['Accept'] = 'application/vnd.github+json'
      req.header['Content-Type'] = 'application/json'
      req.header['X-GitHub-Api-Version'] = '2022-11-28'
      req.header['X-OAuth-Scopes'] = 'repo, user'
      req.header['X-Accepted-OAuth-Scopes'] = 'repo'
      req.header['Authorization'] =
        'Bearer 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'
      req.body = JSON.stringify({
        owner: 'chaunceyTap',
        repo: 'test3',
        base_tree: baseTreeSha,
        tree: [
          {
            path: newResult[0],
            mode: '100644',
            type: 'blob',
            content: newResult[1],
          },
        ],
      })

      req.execute()

      var response = req.response

      var body = response.body
      var bodyAsJson = JSON.parse(body)
      // logInfo(body);

      var newTreeSha = bodyAsJson.sha
      logInfo('This is the new tree sha:   ' + newTreeSha)
      //logInfo(newResult);
      function commitToTree(newTreeSha, baseTreeSha) {
        var URL = 'https://api.github.com/repos/TAP-CXM/TAPSandbox/git/commits'
        var req = new HttpClientRequest(URL)

        req.method = 'POST'

        req.header['User-Agent'] = 'chaunceyTAP'
        req.header['Accept'] = 'application/vnd.github+json'
        req.header['Content-Type'] = 'application/json'
        req.header['X-GitHub-Api-Version'] = '2022-11-28'
        req.header['X-OAuth-Scopes'] = 'repo, user'
        req.header['X-Accepted-OAuth-Scopes'] = 'repo'
        req.header['Authorization'] =
          'Bearer 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'

        req.body = JSON.stringify({
          parents: [baseTreeSha],
          tree: newTreeSha,
          message: 'Recurring commit from Adobe Campaign Classic',
        })

        req.execute()

        var response = req.response

        var body = response.body
        var bodyAsJson = JSON.parse(body)

        var newShaCommit = bodyAsJson.sha

        function pushToRepo(newShaCommit) {
          var URL =
            'https://api.github.com/repos/TAP-CXM/TAPSandbox/git/refs/heads/main'
          var req = new HttpClientRequest(URL)

          req.method = 'POST'

          req.header['User-Agent'] = 'chaunceyTAP'
          req.header['Accept'] = 'application/vnd.github+json'
          req.header['Content-Type'] = 'application/json'
          req.header['X-GitHub-Api-Version'] = '2022-11-28'
          req.header['X-OAuth-Scopes'] = 'repo, user'
          req.header['X-Accepted-OAuth-Scopes'] = 'repo'
          req.header['Authorization'] =
            'Bearer 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'

          req.body = JSON.stringify({ sha: newShaCommit, force: true })

          req.execute()

          var body = response.body
          var bodyAsJson = JSON.parse(body)

          document.write(body)
          logInfo(body)
        }

        pushToRepo(newShaCommit)
      }
      commitToTree(newTreeSha, baseTreeSha)
    }
    createTree(baseTreeSha, treeSha)
  }
  viewCommit(baseTreeSha)

  logInfo(' You have successfully pushed a package to github')
}

getBranches()
