<template>
  <div class="row justify-content-center" id="runName">
    <div class="col">
      <h6 id="Run1Name" style="text-align: center;"></h6>
    </div>
    <div class="col">
      <h6 id="Run2Name" style="text-align: center;"></h6>
    </div>
  </div>
  <div class="row" v-for="run in rendered_run">
    <div class="card" style="width: 95%">
      <div class="card-header">
        <div class="docid" style="right: 0px; width=100%"><div class="docid-value">{{ run.doc_id }}</div></div>
        <h6 class="badge badge-info" title="Relevant" style="cursor: help;">Rel: {{run.relevance}}</h6>
        <h6 class="badge">Score: {{run.score}}</h6>
        <div class="snippet">
          <div><span style="color: #999;" v-html="run.snippet"/></div>
        </div>
      </div>
    </div>
  </div>    
</template>

<script lang="ts">
function markup(text, weights) {
  weights = weights.filter(function (e) {
    return (e[2] > 0 || typeof e[2] === 'string');
  })

  if (weights.length === 0) {
    return '<div>' + text + '</div>'
  }

  var ret = text.substring(0, weights[0][0])
  for (let i: number in weights) {
    i = parseInt(i)
    let weight = weights[i]
    if (typeof weight[2] === 'string') {
      var weightColor = weight[2];
    } else {
      var weightColor = 'rgba(255, 237, 140, ' + weight[2].toString() + ')';
    }

    ret += '<mark background="' + weightColor + ' run1="' + weight[3] + '" run2="0">' + text.substring(weight[0], weight[1]) + '</mark>'

    if (i + 1 < weights.length) {
      ret += '<span>' + text.substring(weight[1], weights[i + 1][0]) + '</span>'
    }
  }

  ret += '<span>' + text.substring(weights[weights.length - 1][1], text.length) + '</span>'

  return '<div><span>' + ret + '</span></div>'
}

function colorizeWeights(mergedWeights) {
  // deep copu & handle if doesn't exist
  mergedWeights = mergedWeights ? JSON.parse(JSON.stringify(mergedWeights)) : [];
  var results = mergedWeights.map((segment) => {
  if (!("run2" in segment[2]) || segment[2].run2 === null) {
    return [segment[0], segment[1], 'rgba(' + COLOR_A + ', ' + segment[2].run1.toString() + ')', segment[2].run1, segment[2].run2];
  } else if (!("run" in segment[2]) || segment[2].run1 === null) {
    return [segment[0], segment[1], 'rgba(' + COLOR_B + ', ' + segment[2].run2.toString() + ')', segment[2].run1, segment[2].run2];
  } else {
    var nil = 'rgba(0, 0, 0, 0)'
    var colorA = 'rgba(' + COLOR_A + ', ' + segment[2].run1.toString() + ')';
    var colorB = 'rgba(' + COLOR_B + ', ' + segment[2].run2.toString() + ')';
    var overlapColors = 'linear-gradient(' + colorA + ', ' + nil + '), linear-gradient(' + nil + ', ' + colorB + ')'
    return [segment[0], segment[1], overlapColors, segment[2].run1, segment[2].run2];
   }
  })

  return results;
}

  export default {
    name: "diff-ir",
    props: ['run', 'reference_run', 'docs'],
    data() {
      return {
        allWeightsA: {},
        allWeightsB: {},
        mergedWeights: {},
        COLOR_A: '236, 154, 8',
        COLOR_B: '121, 196, 121',
        meta: {
          'relevanceColors': {
            '0': [],
            '1': ["#d54541"],  // red
            '2': ["#6c272a", "#d54541"],  // dark red, red
            '3': ["#6c272a", "#d54541", "#c7797a"],  // dark red, red, light red
          },
          'qrelDefs': {0: 'Not Relevant', 1: 'Related', '2': 'Relevant', '3': 'Highly Relevant'},
        }
      }
    },
    computed: {
      rendered_run() {
        var ret = []
        for(let i of this.run) {
          let doc = this.docs[i.doc_id]
          ret.push({
            'score': i['score'],
            'doc_id': i['doc_id'],
            'snippet': markup(doc['snippet'], doc['weights'])
          })
        }

        return ret
      }
    },
    
    methods: {
    generateDocList(run, otherRun, container, docIdFloat, allWeights) {
      let relevanceColors = this.meta.relevanceColors
      let qrelDefs = this.meta.qrelDefs
      let docs = this.meta.docs

      $.each(run, function (i, doc) {
        allWeights[doc.doc_id] = doc.weights;
        if (i >= 1 && run[i - 1].rank + 1 != doc.rank) {
          $('<div class="elip"></div>').text('? ' + (doc.rank - run[i - 1].rank - 1).toString() + ' doc(s) skipped').appendTo(container);
        }
        var $did = $('<div class="docid"></div>').append($('<div class="docid-value"></div>').text(doc.doc_id));
        var doc_fields = docs[doc.doc_id];
        var rel = doc_fields && doc_fields['relevance'] !== null ? doc_fields['relevance'].toString() : 'null';

        $did.css('background-color', relevanceColors[rel]).css(docIdFloat, '0');
        if (rel === null) {
          var $rel = $('<h6 class="badge badge-info">Unjudged</h6>').css('background-color', relevanceColors['null']);
        } else {
          var $rel = $('<h6 class="badge badge-info"></h6>').text('Rel: ' + rel).css('background-color', relevanceColors[rel]).attr('title', qrelDefs[rel]).css('cursor', 'help');
        }
        var $score = $('<h6 class="badge"></h6>').text('Score: ' + doc.score.toFixed(4));
        
        var $text = markup(doc_fields[doc.snippet.field].substring(doc.snippet.start, doc.snippet.stop), doc.snippet.weights)
        if (doc.snippet.stop < doc_fields[doc.snippet.field].length) {
          $text.append('...');
        }
        if (doc.snippet.start > 0) {
          $text.prepend('...');
        }
        $text.prepend($('<span style="color: #999;"></span>').text(doc.snippet.field + ': '));
        // $text.append(' ').append('<a href="#" class="doc-info" role="button">See more</a>');
        var otherRank = null;
        $.each(otherRun, function (i, otherDoc) {
          if (otherDoc.doc_id === doc.doc_id) {
            otherRank = otherDoc.rank;
            return false; // break
          }
        });
        if (otherRank === null) {
          var symbol = '×';
          var tip = 'not ranked in other run';
        }
        else if (doc.rank === otherRank) {
          var symbol = docIdFloat === 'right' ? '?' : '?';
          var tip = 'ranked equally in other run'
        } else if (doc.rank < otherRank) {
          var symbol = docIdFloat === 'right' ? '?' : '?';
          var tip = 'ranked lower in other run (' + otherRank + ')'
        } else if (doc.rank > otherRank) {
          var symbol = docIdFloat === 'right' ? '?' : '?';
          var tip = 'ranked higher in other run (' + otherRank + ')'
        }
        var newEl = $('<div></div>')
          // .append($('<span class="other-rank"></span>').text(symbol).css('float', docIdFloat).css('text-align', docIdFloat === 'right' ? 'left' : 'right').attr('title', tip))
          .append($('<div class="card"></div>')
            .attr("run1-rank", docIdFloat === 'right' ? doc.rank : (otherRank === null ? "No" : otherRank))
            .attr("run2-rank", docIdFloat === 'right' ? (otherRank === null ? "No" : otherRank): doc.rank)
            .attr('data-docid', doc.doc_id)
            .append($('<div class="card-header"></div>')
              .css('padding-' + docIdFloat, '30px')
              .append($("<span class='border badge' style='min-width: 50px; font-weight: normal;color: grey;'></span>").html('<span style="font-size: 1.2em;font-weight:bold; color: black;">'+doc.rank +'</span> '+symbol + (otherRank === null ? '': otherRank)).attr('title', tip))
              .append(' ')
              .append($did)
              .append(' ')
              .append($rel)
              .append(' ')
              .append($score)
              .append($('<div class="snippet"></div>').append($text))
            )
          )
          .appendTo(container);
      });
    }

    }
  }
</script>


<style scoped>
    .card {
      margin: 5px !important;
    }

    .highlight {
      background-color: #ffffd3;
    }

    #DocumentOverlay {
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      background-color: rgba(0, 0, 0, .25);
    }

    #DocumentDetails {
      position: fixed;
      top: 60px;
      left: 10%;
      right: 10%;
      bottom: 60px;
      background-color: white;
      padding: 20px;
      border: 1px solid rgba(0, 0, 0, .125);
      border-radius: 0.25rem;
      box-shadow: 0 0 16px black;
      overflow: auto;
    }

    .close-overlay {
      position: absolute;
      top: 4px;
      right: 4px;
      border-radius: 100%;
      background-color: #111;
      font-size: 17px;
      padding: 9px;
      color: white;
      width: 30px;
      height: 30px;
      text-align: center;
      font-weight: normal;
      line-height: 11px;
      cursor: pointer;
    }

    .docid {
      background-color: rgb(224, 135, 55);
      position: absolute;
      top: 0;
      bottom: 0;
      width: 20px;
      overflow: hidden;
      margin-bottom: 0;
      border-radius: 0;
      font-weight: normal;
      white-space: nowrap;
    }

    .docid-value {
      transform: rotate(90deg);
      font-size: 0.7em;
      padding-left: 8px;
    }

    .fields th {
      vertical-align: top;
      text-align: right;
      padding-right: 12px;
      color: #999;
      font-weight: normal;
    }

    #query-container {
      max-width: 600px;
      border: 1px solid #999;
      border-radius: 0.25rem;
      margin: 20px auto;
      padding: 10px;
    }

    .other-rank {
      font-size: 1.2em;
      display: inline-block;
      width: 20px;
      margin-top: 46px;
      margin-left: 3px;
      margin-right: 3px;
      cursor: help;
    }

    mark {
      padding: 0;
      font-weight: bold;
    }

    .snippet {
      font-size: 0.9em;
      line-height: 1.2;
    }

    .elip {
      text-align: center;
      margin: 16px;
      color: gray;
    }

    .doc-info {
      white-space: nowrap;
    }

    .card-header {
      min-height: 128px;
      cursor: pointer;
    }

    .swatch {
      display: inline-block;
      width: 16px;
      height: 16px;
      vertical-align: middle;
    }

    .form-group {
      width: 150px;
      height: 20px;
      padding-left: 10px;
      padding-top: 10px;
    }

    .nobackground {
      background: transparent !important;
      font-weight: normal;
    }
    .styled-table {
      margin-left: 0px;
      margin-top: 10px;
      border-collapse: collapse;    
      font-size: 0.9em;
      /* font-family: sans-serif;       */
      min-width: 350px;      
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    .styled-table thead tr {
      background-color: #17a2b8;
      color: #ffffff;
      text-align: left;
    }    
    /* .styled-table th, */
    .styled-table td {
      /* padding: 12px 15px; */
      text-align: center;
    }    
    .styled-table tbody tr {
      color: #ffffff;
    }
    /*
    .styled-table tbody tr:nth-of-type(even) {
      background-color: #f3f3f3;
    } */

    .styled-table tbody tr:last-of-type {
      border-bottom: 2px solid #009879;
    }

    #ranking-summary ul li span {
      margin-right: 5px;
    }    
</style>