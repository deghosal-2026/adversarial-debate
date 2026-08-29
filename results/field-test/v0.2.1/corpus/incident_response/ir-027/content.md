<!DOCTYPE html>
<html lang="en">
  <head>
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0], j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src= 'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f); })(window,document,'script','dataLayer','GTM-WVF23W3');</script>
    <meta charset="utf-8">
    <meta content="initial-scale=1, minimum-scale=1, width=device-width" name="viewport">
    <title>Google SRE - Postmortem Practices for Incident Management</title>
      <meta name="description" content="SRE postmortem practices for documenting incidents, understanding root causes, and preventing recurrence. Explore blameless postmortemculture and best practices.">
    <meta name="referrer" content="no-referrer" />
    <link rel="canonical" href="https://sre.google/workbook/postmortem-culture/">
    <link rel="apple-touch-icon-precomposed" sizes="180x180" href="https://lh3.googleusercontent.com/Yf2DCX8RKda6r4Jml9DLMByS2zQCBFs3kQpvBfN8UgIh4YVWIYSYIQOoTxJriyuM26cT5PDjyEb5aynDQ0Xyz46yHKnfg8JlUbDW">
    <link rel="stylesheet" href="//fonts.googleapis.com/css?family=Google+Sans:400|Roboto:400,400italic,500,500italic,700,700italic|Roboto+Mono:400,500,700|Material+Icons">
    <link rel="icon" type="image/png" sizes="32x32" href="https://lh3.googleusercontent.com/Yf2DCX8RKda6r4Jml9DLMByS2zQCBFs3kQpvBfN8UgIh4YVWIYSYIQOoTxJriyuM26cT5PDjyEb5aynDQ0Xyz46yHKnfg8JlUbDW">
    <link rel="icon" type="image/png" sizes="16x16" href="https://lh3.googleusercontent.com/Yf2DCX8RKda6r4Jml9DLMByS2zQCBFs3kQpvBfN8UgIh4YVWIYSYIQOoTxJriyuM26cT5PDjyEb5aynDQ0Xyz46yHKnfg8JlUbDW">
    <link rel="shortcut icon" href="https://lh3.googleusercontent.com/Yf2DCX8RKda6r4Jml9DLMByS2zQCBFs3kQpvBfN8UgIh4YVWIYSYIQOoTxJriyuM26cT5PDjyEb5aynDQ0Xyz46yHKnfg8JlUbDW">
    <link href="/sre-book/static/css/index.min.css?cache=6c30b59" rel="stylesheet">
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-75468017-1', 'auto');
      ga('send', 'pageview');
    </script>
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "/workbook/postmortem-culture/"
      },
      "headline": "Postmortem Culture: Learning from Failure",
      "description": "Introducing postmortems into an organization is as much a cultural change as it is a technical one. Making such a shift can seem daunting. The key takeaway from this chapter is that making this change is possible, and needn't seem like an insurmountable challenge.",
        "image": "https://lh3.googleusercontent.com/L4hSmfujS0jXPgjFwTc0LdMQwLchtsPJLm86A2z6nH23ykrj0Sw39gQPtRwl37sFZ0XaZGysiBMhK6gJc1p-Pq12sDHM-fYmvSTH",
        "author": [
            {
              "@type": "Person",
              "name": "Daniel Rogers"
            },
            {
              "@type": "Person",
              "name": "Murali Suriar"
            },
            {
              "@type": "Person",
              "name": "Sue Lueder"
            },
            {
              "@type": "Person",
              "name": "Pranjal Deo"
            },
            {
              "@type": "Person",
              "name": "Divya Sudhakar"
            },
            {
              "@type": "Person",
              "name": "Gary O&#39;Connor"
            },
            {
              "@type": "Person",
              "name": "Dave Rensin"
            }
        ],
      "publisher": {
        "@type": "Organization",
        "name": "Google SRE",
        "logo": {
          "@type": "ImageObject",
          "url": "https://lh3.googleusercontent.com/C3_YVnTdc7xzTDekhsGeZ2hEYUnAlp47Au-9C50vi5r44rfpJAgiycs1g6AFKWqIpw6KVPrZWLse1VUqgOqYht-RxV1iowdB0_IABUd966aDsDWW-65m"
        }
      }
    }
  </script>
    <script src="/sre-book/static/js/detect.min.js?cache=4cb778b"></script>
  </head>

  <body>
    <noscript><iframe class="no-script-iframe" src="https://www.googletagmanager.com/ns.html?id=GTM-WVF23W3"></iframe></noscript>
    <main>
  <div ng-controller= "HeaderCtrl as headerCtrl">
    <div id="curtain" class="menu-closed"></div>
      <div class="header clearfix">
        <a id="burger-menu" class="expand"></a>
        <h2 class="chapter-title">
                Chapter 10 - Postmortem Culture: Learning from Failure
        </h2>
      </div>
      <div id="overlay-element" class="expands">
        <div class="logo">
          <a href="https://www.google.com"><img src="https://lh3.googleusercontent.com/YoVRtLOHMSRYQZ3OhFL8RIamcjFYbmQXX4oAQx02MRqqY9zlKNvsuZpS73khXiOqTH3qrFW27VrERJJIHTjPk-tAh46q8-Fd4w6qlw" alt="Google"></a>
        </div>
        <ol id="drop-down" class="dropdown-content hide">
          <li><a class="menu-buttons" href="/workbook/table-of-contents/">Table of Contents</a></li>
            <li>
              <a href="/workbook/foreword-I/" class="menu-buttons">
                  Foreword I
              </a>
            </li>
            <li>
              <a href="/workbook/foreword-II/" class="menu-buttons">
                  Foreword II
              </a>
            </li>
            <li>
              <a href="/workbook/preface/" class="menu-buttons">
                  Preface
              </a>
            </li>
            <li>
              <a href="/workbook/how-sre-relates/" class="menu-buttons">
                  1. How SRE Relates to DevOps
              </a>
            </li>
            <li>
              <a href="/workbook/part-I-foundations/" class="menu-buttons">
                  Part I - Foundations
              </a>
            </li>
            <li>
              <a href="/workbook/implementing-slos/" class="menu-buttons">
                  2. Implementing SLOs
              </a>
            </li>
            <li>
              <a href="/workbook/slo-engineering-case-studies/" class="menu-buttons">
                  3. SLO Engineering Case Studies
              </a>
            </li>
            <li>
              <a href="/workbook/monitoring/" class="menu-buttons">
                  4. Monitoring
              </a>
            </li>
            <li>
              <a href="/workbook/alerting-on-slos/" class="menu-buttons">
                  5. Alerting on SLOs
              </a>
            </li>
            <li>
              <a href="/workbook/eliminating-toil/" class="menu-buttons">
                  6. Eliminating Toil
              </a>
            </li>
            <li>
              <a href="/workbook/simplicity/" class="menu-buttons">
                  7. Simplicity
              </a>
            </li>
            <li>
              <a href="/workbook/part-II-practices/" class="menu-buttons">
                  Part II - Practices
              </a>
            </li>
            <li>
              <a href="/workbook/on-call/" class="menu-buttons">
                  8. On-Call
              </a>
            </li>
            <li>
              <a href="/workbook/incident-response/" class="menu-buttons">
                  9. Incident Response
              </a>
            </li>
            <li class="active">
              <a href="/workbook/postmortem-culture/" class="menu-buttons">
                  10. Postmortem Culture: Learning from Failure
              </a>
            </li>
            <li>
              <a href="/workbook/managing-load/" class="menu-buttons">
                  11. Managing Load
              </a>
            </li>
            <li>
              <a href="/workbook/non-abstract-design/" class="menu-buttons">
                  12. Introducing Non-Abstract Large System Design
              </a>
            </li>
            <li>
              <a href="/workbook/data-processing/" class="menu-buttons">
                  13. Data Processing Pipelines
              </a>
            </li>
            <li>
              <a href="/workbook/configuration-design/" class="menu-buttons">
                  14. Configuration Design and Best Practices
              </a>
            </li>
            <li>
              <a href="/workbook/configuration-specifics/" class="menu-buttons">
                  15. Configuration Specifics
              </a>
            </li>
            <li>
              <a href="/workbook/canarying-releases/" class="menu-buttons">
                  16. Canarying Releases
              </a>
            </li>
            <li>
              <a href="/workbook/part-III-processes/" class="menu-buttons">
                  Part III - Processes
              </a>
            </li>
            <li>
              <a href="/workbook/overload/" class="menu-buttons">
                  17. Identifying and Recovering from Overload
              </a>
            </li>
            <li>
              <a href="/workbook/engagement-model/" class="menu-buttons">
                  18. SRE Engagement Model
              </a>
            </li>
            <li>
              <a href="/workbook/reaching-beyond/" class="menu-buttons">
                  19. SRE: Reaching Beyond Your Walls
              </a>
            </li>
            <li>
              <a href="/workbook/team-lifecycles/" class="menu-buttons">
                  20. SRE Team Lifecycles
              </a>
            </li>
            <li>
              <a href="/workbook/organizational-change/" class="menu-buttons">
                  21. Organizational Change Management in SRE
              </a>
            </li>
            <li>
              <a href="/workbook/conclusion/" class="menu-buttons">
                  Conclusion
              </a>
            </li>
            <li>
              <a href="/workbook/slo-document/" class="menu-buttons">
                  Appendix A. Example SLO Document
              </a>
            </li>
            <li>
              <a href="/workbook/error-budget-policy/" class="menu-buttons">
                  Appendix B. Example Error Budget Policy
              </a>
            </li>
            <li>
              <a href="/workbook/postmortem-analysis/" class="menu-buttons">
                  Appendix C. Results of Postmortem Analysis
              </a>
            </li>
            <li>
              <a href="/workbook/index/" class="menu-buttons">
                  Index
              </a>
            </li>
            <li>
              <a href="/workbook/editors/" class="menu-buttons">
                  About the Editors
              </a>
            </li>
            <li>
              <a href="/workbook/colophon/" class="menu-buttons">
                  Colophon
              </a>
            </li>
        </ol>
      </div>
    </div>

  <div id="maia-main">
    <div class="content" id="content">
      <h1 class="heading jumptargets" id="postmortem-culture-learning-from-failure">Postmortem Culture: Learning from Failure</h1>

<p class="byline author">By Daniel Rogers, Murali Suriar, Sue Lueder,<br>Pranjal Deo, and Divya Sudhakar<br>with Gary O’Connor and Dave Rensin
</p>

<p>
  Our experience shows that a truly blameless postmortem culture results in more reliable systems—which is why we believe this practice is important to creating and maintaining a successful SRE organization.
</p>

<p>
  Introducing postmortems into an organization is as much a cultural change as it is a technical one. Making such a shift can seem daunting. The key takeaway from this chapter is that making this change is possible, and needn’t seem like an insurmountable challenge. Don’t emerge from an incident hoping that your systems will eventually remedy themselves. You can start small by introducing a very basic postmortem procedure, and then reflect and tune your process to best suit your organization—as with many things, there is no one size that fits all.
</p>

<p>
  When written well, acted upon, and widely shared, postmortems can be a very effective tool for driving positive organizational change and preventing repeat outages. To illustrate the principles of good postmortem writing, this chapter presents a case study of an actual outage that happened at Google. An example of a poorly written postmortem highlights the reasons why “bad” postmortem practices are damaging to an organization that’s trying to create a healthy postmortem culture. We then compare the bad postmortem with the actual postmortem that was written after the incident, highlighting the principles and best practices of a high-quality postmortem.
</p>

<p>
  The second part of this chapter shares what we’ve learned about creating incentives for nurturing of a robust postmortem culture and how to recognize (and remedy) the early signs that the culture is breaking down.
</p>

<p>
  Finally, we provide tools and templates that you can use to bootstrap a postmortem culture.
</p>

<p>
  For a comprehensive discussion on blameless postmortem philosophy, see <a href="https://sre.google/sre-book/postmortem-culture/">Chapter 15</a> in our first book, <span class="italic">Site Reliability Engineering</span>.
</p>

<h2 class="heading jumptargets" id="case-study">Case Study</h2>

<p>
  This case study features a routine rack decommission that led to an increase in service latency for our users. A bug in our maintenance automation, combined with insufficient rate limits, caused thousands of servers carrying production traffic to simultaneously go offline.
</p>

<p>
  While the majority of Google’s servers are located in our proprietary datacenters, we also have racks of proxy/cache machines in colocation facilities (or “colos”). Racks in colos that contain our proxy machines are called <span class="italic">satellites</span>. Because satellites undergo regular maintenance and upgrades, a number of satellite racks are being installed or decommissioned at any point in time. At Google, these maintenance processes are largely automated.
</p>

<p>
  The decommission process overwrites the full content of all drives in the rack using a process we call <span class="italic">diskerase</span>. Once a machine is sent to diskerase, the data it once stored is no longer retrievable. The steps for a typical rack decommission are as follows:
</p>

<pre class="code-indentation">

# Get all active machines in "satellite"
machines = GetMachines(satellite)

# Send all candidate machines matching "filter" to decom
SendToDecom(candidates=GetAllSatelliteMachines(),
            filter=machines)

</pre>

<p>
  Our case study begins with a satellite rack that was marked for decommissioning. The diskerase step of the decommission process finished successfully, but the automation responsible for the remainder of the machine decommission failed. To debug the failure, we retried the decommission process. The second decommission ran as follows:
</p>

<pre class="code-indentation">
# Get all active machines in "satellite"
machines = GetMachines(satellite)
<em>
# "machines" is an empty list, because the decom flow has already run.
# API bug: an empty list is treated as "no filter", rather than "act on no
# machines"
</em>
# Send all candidate machines matching "filter" to decom
SendToDecom(candidates=GetAllSatelliteMachines(),
            filter=machines)

# Send all machines in "candidates" to diskerase.

</pre>

<p>
  Within minutes, the disks of all satellite machines, globally, were erased. The machines were rendered inert and could no longer accept connections from users, so subsequent user connections were routed directly to our datacenters. As a result, users experienced a slight increase in latency. Thanks to good capacity planning, very few of our users noticed the issue during the two days it took us to reinstall machines in the affected colo racks. Following the incident, we spent several weeks auditing and adding more sanity checks to our automation to make our decommission workflow idempotent.
</p>

<p>
  Three years after this outage, we experienced a similar incident: a number of satellites were drained, resulting in increased user latency. The action items implemented from the original postmortem dramatically reduced the blast radius and rate of the second incident.
</p>

<p>
  Suppose you were the person responsible for writing the postmortem for this case study. What would you want to know, and what actions would you propose to prevent this outage from happening again?
</p>

<p>
  Let’s start with a not-so-great postmortem for this incident.
</p>

<h1 class="heading jumptargets" id="bad-postmortem">Bad Postmortem</h1>

<aside data-type="sidebar" class="highlight pagebreak-before" id="all-satellite-machines-sent-to-diskerase">
  <h5 class="subheaders jumptargets" align="center">Postmortem: All Satellite Machines Sent to Diskerase</h5>
<em>2014-August-11</em>
<p>
  <em>Owner: </em>maxone@, logantwo@, sydneythree@, dylanfour@
</p>
<p>
  <em>Shared with: </em>satellite-infra-team@
</p>
<p>
  <em>Status: </em>Final
</p>
<p>
  <em>Incident date: </em>2014-August-11
</p>
<p>
  <em>Published: </em>2014-December-30
</p>
<p><em>Executive Summary</em></p>
<p>
  <em>Impact: </em>All Satellite machines are sent to diskerase, which practically wiped out Google Edge.
</p>
<p>
  <em>Root cause: </em>dylanfour@ ignored the automation setup and ran the cluster turnup logic manually, which triggered an existing bug.
</p>
<p>
  <em>Problem Summary</em>
</p>
<p>
  <em>Duration of problem: </em>40min
</p>
<p>
  <em>Product(s) affected: </em>satellite-infra-team
</p>
<p>
  <em>% of product affected: </em>All satellite clusters.
</p>
<p>
  <em>User impact: </em>All queries that normally go to satellites were served from the core instead, causing increased latency.
</p>
<p>
  <em>Revenue impact: </em>Some ads were not served due to the lost queries. Exact revenue impact unknown at this time.
</p>
<p>
  <em>Detection:</em>Monitoring alert.
</p>
<p>
  <em>Resolution:</em>Diverting traffic to core followed by manual repair of edge clusters.
</p>
<p>
  <em>Background (optional)</em>
</p>
<p>
  <em>Impact</em>
</p>
<p class="italic">
  User impact
</p>
<ul class="simplelist">
  <li>
    All queries that normally go to satellites were instead served from the core, causing increased latency to user traffic.
  </li>
</ul>
<p class="italic">Revenue impact</p>
<ul class="simplelist">
  <li>
    Some ads were not served due to the lost queries.
  </li>
</ul>
<p>
  <em>Root Causes and Trigger</em>
</p>
<p>
  Cluster turnup/turndown automation is not meant to be idempotent. The tool has safeguards to ensure that certain steps cannot be run more than once. Unfortunately, there is nothing to stop someone from running the code manually as many times as they want. None of the documentation mentioned this gotcha. As a result, most team members think it’s okay to run the process multiple times if it doesn’t work.
</p>
<p>
  This is exactly what happened during a routine decommissioning of a rack. The rack was being replaced with a new Iota-based satellite. dylanfour@ completely ignored the fact that the turnup had already executed once and was stuck in the first attempt. Due to careless ignorance, they triggered a bad interaction that assigned all the satellite machines to the diskerase team.
</p>
<p><em>Recovery Efforts</em></p>
<p><em>Lessons Learned</em></p>
<p>Things that went well</p>
<ul>
  <li>
    Alerting caught the issue immediately.
  </li>
  <li>
    Incident management went well.
  </li>
</ul>
<p>Things that went poorly</p>
<ul>
  <li>
    The team (especially maxone@, logantwo@) never wrote any documentation to tell SREs not to run the automation multiple times, which is ridiculous.
  </li>
  <li>
    On-call did not act soon enough to prevent most satellite machines from being erased. This is not the first time that on-call failed to react in time.
  </li>
</ul>
<p>Where we got lucky</p>
<ul>
  <li>
    Core was able to serve all the traffic that normally would have gone to the Edge. I can’t believe we survived this one!!!
  </li>
</ul>
<p><em>Action Items</em></p>
<table>
    <thead>
        <tr>
          <th>Action Item</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Tracking Bug</th>
        </tr>
    </thead>
      <tbody>
        <tr>
          <td><p>Make automation better.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P2</p></td>
          <td><p>logantwo@</p></td>
          <td></td>
        </tr>
        <tr>
            <td><p>Improve paging and alerting.</p></td>
            <td><p>detect</p></td>
            <td><p>P2</p></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
          <td><p>sydneythree@ needs to learn proper cross-site handoff protocol so nobody has to work on duplicate issues.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P2</p></td>
          <td></td>
          <td><p>BUG6789</p></td>
        </tr>
        <tr>
          <td><p>Train humans not to run unsafe commands.</p></td>
          <td><p>prevent</p></td>
          <td><p>P2</p></td>
          <td></td>
          <td></td>
        </tr>
     </tbody>
</table>
<p><em>Glossary</em></p>
</aside>

<h5 class="subheaders jumptargets" id="why-is-this-postmortem-bad">Why Is This Postmortem Bad?</h5>

<p>The example “bad” postmortem contains a number of common failure modes that we try to avoid. The following sections explain how to improve upon this postmortem.</p>

<h6 class="subheaders-small jumptargets" id="missing-context">Missing context</h6>

<p>
  From the outset, our <a href="../../sre-book/example-postmortem/">example postmortem</a> introduces terminology that’s specific to traffic serving (e.g., “satellites”) and lower layers of machine management automation at Google (e.g., “diskerase”). If you need to provide additional context as part of the postmortem, use the Background and/or Glossary sections (which can link to longer documents). In this case, both sections were blank.
</p>

<p>
  If you don’t properly contextualize content when <a href="https://sre.google/sre-book/example-postmortem/">writing a postmortem</a>, the document might be misunderstood or even ignored. It’s important to remember that your audience extends beyond the immediate team.
</p>

<h6 class="subheaders-small jumptargets" id="key-details-omitted">Key details omitted</h6>

<p>
  Multiple sections contain high-level summaries but lacked important details. For example:
</p>

<p class="italic">Problem summary</p>

<ul class="simplelist">
  <li>For outages affecting multiple services, you should present <a href="https://sre.google/workbook/postmortem-analysis/">numbers to give a consistent representation</a> of impact. The only numerical data our example provides is the duration of the problem. We don’t have enough details to estimate the size or impact of the outage. Even if there is no concrete data, a well-informed estimate is better than no data at all. After all, if you don’t know how to measure it, then you can’t know it’s fixed!</li>
</ul>

<p class="italic">Root causes and trigger</p>

<ul class="simplelist">
  <li>
    Identifying the root causes and trigger is one of the most important reasons to write a postmortem. Our example contains a small paragraph that describes the root causes and trigger, but it doesn’t explore the lower-level details of the issue.
  </li>
</ul>

<p class="italic">Recovery efforts</p>

<ul class="simplelist">
  <li>
    A postmortem acts as the record of an incident for its readers. A good postmortem will let readers know what happened, how the issue was mitigated, and how users were impacted. The answers to many of these questions are typically found in the Recovery Efforts section, which was left empty in our example.
  </li>
</ul>

<p>
  If an outage merits a postmortem, you should also take the time to accurately capture and document the necessary details. The reader should get a complete view of the outage and, more importantly, learn something new.
</p>

<h6 class="subheaders-small jumptargets" id="key-action-item-characteristics-missing">Key action item characteristics missing</h6>

<p>
  The Action Items (AIs) section of our example is missing the core aspects of an actionable plan to prevent recurrence. For example:
</p>

<ul>
  <li>
    The action items are mostly mitigative. To minimize the likelihood of the outage recurring, you should include some preventative action items and fixes. The one “preventative” action item suggests we “make humans less error-prone.” In general, trying to change human behavior is less reliable than changing automated systems and processes. (Or as Dan Milstein <a href="https://product.hubspot.com/blog/bid/64771/Post-Mortems-at-HubSpot-What-I-Learned-From-250-Whys" target="_blank" rel="noopener noreferrer">once quipped</a>: “Let’s plan for a future where we’re all as stupid as we are today.”)
  </li>
  <li>
    All of the action items have been tagged with an equal priority. There’s no way to determine which action to tackle first.
  </li>
  <li>
    The first two action items in the list use ambiguous phrases like “Improve” and “Make better.” These terms are vague and open to interpretation. Using unclear language makes it difficult to measure and understand success criteria.
  </li>
  <li>
    Only one action item was assigned a tracking bug. Without a formal tracking process, action items from postmortems are often forgotten, resulting in outages.
  </li>
</ul>

<aside data-type="sidebar" class="highlight pagebreak-before note-highlight">
<h6 class="subheaders-small jumptargets" id="note-1" align="center">Note</h6>
<p class="note">
  In the words of Ben Treynor Sloss, Google’s VP for 24/7 Operations: “To our users, a postmortem without subsequent action is indistinguishable from no postmortem. Therefore, all postmortems which follow a user-affecting outage must have at least one P[01] bug associated with them. I personally review exceptions. There are very few exceptions.”
</p>
</aside>

<h6 class="subheaders-small jumptargets" id="counterproductive-finger-pointing">Counterproductive finger pointing</h6>

<p>
  Every postmortem has the potential to lapse into a blameful narrative. Let’s take a look at some examples:
</p>

<p class="italic">Things that went poorly</p>

<ul class="simplelist">
  <li>
    The entire team is blamed for the outage, while two members (maxone@ and logantwo@) are specifically called out.
  </li>
</ul>

<p class="italic">Action items</p>

<ul class="simplelist">
  <li>
    The last item in the list targets sydneythree@ for succumbing to pressure and mismanaging the cross-site handoff.
  </li>
</ul>

<p class="italic">Root causes and trigger</p>

<ul class="simplelist">
  <li>
    dylanfour@ is held solely responsible for the outage.
  </li>
</ul>

<p>
  It may seem like a good idea to highlight individuals in a postmortem. Instead, this practice leads team members to become risk-averse because they’re afraid of being publicly shamed. They may be motivated to cover up facts critical to understanding and preventing recurrence.
</p>

<h6 class="subheaders-small jumptargets" id="animated-language">Animated language</h6>

<p>
A postmortem is a factual artifact that should be free from personal judgments and subjective language. It should consider multiple perspectives and be respectful of others. Our example postmortem contains multiple examples of undesirable language:
</p>

<p class="italic">Root causes and trigger</p>

<ul class="simplelist">
  <li>
    Superfluous language (e.g., “careless ignorance”)
  </li>
</ul>

<p class="italic">Things that went poorly</p>

<ul class="simplelist">
  <li>
    Animated text (e.g., “which is ridiculous”)
  </li>
</ul>

<p class="italic">Where we got lucky</p>

<ul class="simplelist">
  <li>
    An exclamation of disbelief (e.g., “I can't believe we survived this one!!!”)
  </li>
</ul>

<p>
  Animated language and dramatic descriptions of events distract from the key message and erode psychological safety. Instead, provide verifiable data to justify the severity of a statement.
</p>

<h6 class="subheaders-small jumptargets" id="missing-ownership">Missing ownership</h6>

<p>
  Declaring official ownership results in accountability, which leads to action. Our example postmortem contains several examples of missing ownership:
</p>

<ul>
  <li>
    The postmortem lists four owners. Ideally, an owner is a single point of contact who is responsible for the postmortem, follow-up, and completion.
  </li>
  <li>
    The Action Items section has little or no ownership for its entries. Actions items without clear owners are less likely to be resolved.
  </li>
</ul>

<p>
  It’s better to have a single owner and multiple collaborators.
</p>

<h6 class="subheaders-small jumptargets" id="limited-audience">Limited audience</h6>

<p>
  Our example postmortem was shared only among members of the team. By default, the document should have been accessible to everyone at the company. We recommend proactively sharing your postmortem as widely as possible—perhaps even with your customers. The value of a postmortem is proportional to the learning it creates. The more people that can learn from past incidents, the less likely they are to be repeated. A thoughtful and honest postmortem is also a key tool in restoring shaken trust.
</p>

<p>
  As your experience and comfort grows, you will also likely expand your “audience” to nonhumans. Mature postmortem cultures often add machine-readable tags (and other metadata) to enable downstream analytics.
</p>

<h6 class="subheaders-small jumptargets" id="delayed-publication">Delayed publication</h6>

<p>
  Our example postmortem was published four months after the incident. In the interim, had the incident recurred (which in reality, did happen), team members likely would have forgotten key details that a timely postmortem would have captured.
</p>

<h1 class="heading jumptargets" id="good-postmortem">Good Postmortem</h1>

<aside data-type="sidebar" class="highlight pagebreak-before note-highlight">
<h6 class="subheaders-small jumptargets" id="note-2" align="center">Note</h6>
<p class="note">
  This is an actual postmortem. In some cases, we fictionalized names of individuals and teams. We also replaced actual values with placeholders to protect sensitive capacity information. In the postmortems that you create for your internal consumption, you should absolutely include specific numbers!
</p>
</aside>

<aside data-type="sidebar" class="highlight pagebreak-before" id="all-satellite-machines-sent-to-diskerase">
  <h2 class="subheaders jumptargets" align="center" id="postmortem-all-satellite-machines-sent-to-diskerase">Postmortem: All Satellite Machines Sent to Diskerase</h2>
 <p><em>2014-August-11</em></p>
 <p><em>Owner: </em>Postmortem: maxone@, logantwo@,Datacenter Automation: sydneythree@,Network: dylanfour@,Server Management: finfive@</p>
 <p><em>Shared with: </em><a href="mailto: all_engineering_employees@google.com"><span class="italic"> all_engineering_employees@google.com</span></a></p>
 <p><em>Status: </em>Final</p>
<p><em>Incident date: </em>Mon, August 11, 2014, 17:10 to 17:50 PST8PDT</p>
<p><em>Published: </em>Fri, August 15, 2014</p>
<p><em>Executive Summary</em></p>
<p><em>Impact: </em>Frontend queries dropped,Some ads were not served,There was a latency increase for all services normally served from satellite for nearly two days</p>
<p><em>Root cause: </em>A bug in turndown automation caused all satellite machines, instead of just one rack of satellite machines, to be sent to diskerase. This resulted in all satellite machines entering the decom workflow, which wiped their disks. The result was a global satellite frontend outage.</p>
<p><em>Problem Summary</em></p>
<p><em>Duration of problem: </em>Main outage: Mon, August 11, 17:10 to 17:50 PST8PDT,<p>Reconstruction work and residual pains through Wed, August 13, 07:46 PST8PDT, then the incident was closed.</p></p>
<p><em>Product(s) affected: </em> Frontend Infrastructure, specifically all satellite locations.</p>
<p><em>% of product affected: </em>Global—all traffic normally served from satellites (typically 60% of global queries).</p>
<p><em>User impact: </em>[Value redacted] frontend queries dropped over a period of 40 minutes ([value redacted] QPS averaged over the period, [value redacted] % of global traffic).<p>Latency increase for all services normally served from satellite for nearly two days.</p></p>
<p><em>Revenue impact:</em> The exact revenue impact unknown at this time.</p>
<p><em>Detection: </em>Blackbox alerting: traffic-team was paged with “satellite <code>a12bcd34</code> failing too many HTTP requests” for ~every satellite in the world.</p>
<p><em>Resolution: </em>The outage itself was rapidly mitigated by moving all of Google’s frontend traffic to core clusters, at the cost of additional latency for user traffic.</p>
<p><em>Background (optional)</em></p>
<p>
  If you’re unfamiliar with frontend traffic serving and the lower layers of serving automation at Google, read the glossary before you continue.
</p>
<p><em>Impact</em></p>
<p>User impact</p>
<ul>
  <li>
    [Value redacted] frontend queries dropped over a period of [value redacted] minutes. [Value redacted] QPS averaged over the period, [value redacted] % of global traffic. Our monitoring suggests a much larger crater; however, the data was unreliable as it ceased monitoring satellites that were still serving, thinking they were turned down. The appendix describes how the above numbers were estimated.
  </li>
  <li>
    There was a latency increase for all services normally served from satellite for nearly two days:
  </li>
  <ul>
    <li>
      [Value redacted] ms RTT spikes for countries near core clusters
    </li>
    <li>
      Up to+[value redacted] ms for locations relying more heavily on satellites (e.g., Australia, New Zealand, India)
    </li>
  </ul>
</ul>
<p>Revenue impact</p>
<p>Some ads were not served due to the lost queries. The exact revenue impact is unknown at this time:</p>
<ul>
  <li>
    Display and video: The data has very wide error bars due to day-on-day fluctuations, but we estimate between [value redacted] % and [value redacted] % of revenue loss on the day of the outage.
  </li>
  <li>
    Search: [Value redacted] % to [value redacted] % loss between 17:00 to 18:00, again with wide error bars.
  </li>
</ul>
<p>Team impact</p>
<ul>
  <li>
    The Traffic team spent ~48 hours with all hands on deck rebuilding satellites.
  </li>
  <li>
    NST had a higher-than-normal interrupt/pager load because they needed to traffic-engineer overloaded peering links.
  </li>
  <li>
    Some services may have seen increased responses served at their frontends due to reduced cache hit rate in the GFEs.
  </li>
  <ul>
    <li>
      For example, see this thread [link] about [cache-dependent service].
    </li>
    <li>
      [Cache-dependent service] saw their cache hit rate at the GFEs drop from [value redacted ] % to [value redacted] % before slowly recovering.
    </li>
  </ul>
</ul>
<p>Incident document</p>
<p>[The link to our incident tracking document has been redacted.]</p>
<p><em>Root Causes and Trigger</em></p>
<p>
  A longstanding input validation bug in the Traffic Admin server was triggered by the manual reexecution of a workflow to decommission the <code>a12bcd34</code> satellite. The bug removed the machine constraint on the decom action, sending all satellite machines to decommission.
</p>
<p>
  From there, datacenter automation executed the decom workflow, wiping the hard drives of the majority of satellite machines before this action could be stopped.
</p>
<p>
  The Traffic Admin server provides a <code>ReleaseSatelliteMachines</code> RPC. This handler initiates satellite decommission using three MDB API calls:
</p>
<ul>
  <li>
    Look up the rack name associated with the edge node (e.g., <code>a12bcd34</code> -> &lt;rack name&gt;).
  </li>
  <li>
    Look up the machine names associated with the rack (&lt;rack&gt; -> &lt;machine 1&gt;, &lt;machine 2&gt;, etc.).
  </li>
  <li>
    Reassign those machines to diskerase, which indirectly triggers the decommission workflow.
  </li>
</ul>
<p>
  This procedure is not idempotent, due to a known behavior of the MDB API combined with a missing safety check. If a satellite node was previously successfully sent to decom, step 2 above returns an empty list, which is interpreted in step 3 as the absence of a constraint on a machine hostname.
</p>
<p>
  This dangerous behavior has been around for a while, but was hidden by the workflow that invokes the unsafe operation: the workflow step invoking the RPC is marked “run once,” meaning that the workflow engine will not reexecute the RPC once it has succeeded.
</p>
<p>
  However, “run once” semantics don’t apply across multiple instances of a workflow. When the Cluster Turnup team manually started another run of the workflow for <code>a12bcd34</code>, this action triggered the <code>admin_server</code> bug.
</p>
<p><em>Timeline/Recovery Efforts</em></p>
<p>
  [The link to our Timeline log has been elided for book publication. In a real postmortem, this information would always be included.]
</p>
<p><em>Lessons Learned</em></p>
<p>Things that went well</p>
<ul>
  <li>
    Evacuating the edge. GFEs in core are explicitly capacity-planned to allow this to happen, as is the production backbone (aside from peering links; see the Outage list in the next section). This edge evacuation allowed the Traffic team to mitigate promptly without fear.
  </li>
  <li>
    Automatic mitigation of catastrophic satellite failure. Cover routes automatically pull traffic from failing satellites back to core clusters, and satellites drain themselves when abnormal churn is detected.
  </li>
  <li>
    Satellite decom/diskerase worked very effectively and rapidly, albeit as a <a href="https://en.wikipedia.org/wiki/Confused_deputy_problem" target="_blank" rel="noopener noreferrer">confused deputy</a>.
  </li>
  <li>
    The outage triggered a quick IMAG response via OMG and the tool proved useful for ongoing incident tracking. The cross-team response was excellent, and OMG further helped keep everyone talking to each other.
  </li>
</ul>
<p>
  Things that went poorly
</p>
<p>Outage</p>
<ul>
  <li>
    The Traffic Admin server lacked the appropriate sanity checks on the commands it sent to MDB. All commands should be idempotent, or at least fail-safe on repeat invocations.
  </li>
  <li>
    MDB did not object to the missing hostname constraint in the ownership change request.
  </li>
  <li>
    The decom workflow doesn’t cross-check decom requests with other data sources (e.g., planned rack decoms). As a result, there were no objections to the request to trash (many) geographically diverse machines.
  </li>
  <li>
    The decom workflow is not rate-limited. Once the machines entered decom, disk erase and other decom steps proceeded at maximum speed.
  </li>
  <li>
    Some peering links between Google and the world were overloaded as a result of the egress traffic shifting to different locations when satellites stopped serving, and their queries were instead served from core. This resulted in short bursts of congestion to select peers until satellites were restored, and mitigation work by NST to match.
  </li>
</ul>
<p>Recovery</p>
<ul>
  <li>
    Reinstalls of satellite machines were slow and unreliable. Reinstallations use TFTP to transmit data, which works poorly when transmitting to satellites at the end of high-latency links.
  </li>
  <li>
    The Autoreplacer infrastructure was not able to handle the simultaneous setup of [value redacted] of GFEs at the time of the outage. Matching the velocity of automated setups required the labor of many SREs working in parallel performing manual setups. The factors below contributed to the initial slowness of the automation:
  </li>
  <ul>
    <li>
      Overly strict SSH timeouts prevented reliable Autoreplacer operation on very remote satellites.
    </li>
    <li>
      A slow kernel upgrade process was executed regardless of whether the machine already had the correct version.
    </li>
    <li>
      A concurrency regression in Autoreplacer prevented running more than two machine setup tasks per worker machine.
    </li>
    <li>
      Confusion about the behavior of the Autoreplacer wasted time and effort.
    </li>
  </ul>
  <li>
    The monitoring configuration delta safety checks (25% change) did not trigger when 23% of the targets were removed, but did trigger when the same contents (29% of what remained) were readded. This caused a 30-minute delay in reenabling monitoring of the satellites.
  </li>
  <li>
    “The installer” has limited staffing. As a result, making changes is difficult and slow.
  </li>
  <li>
    Use of superuser powers to claw machines back from diskerase left a lot of zombie state, causing ongoing cleanup pain.
  </li>
</ul>
<p>Where we got lucky</p>
<ul>
  <li>
    GFEs in core clusters are managed very differently from satellite GFEs. As a result, they were not affected by the decom rampage.
  </li>
  <li>
    Similarly, YouTube’s CDN is run as a distinct piece of infrastructure, so YouTube video serving was not affected. Had this failed, the outage would have been much more severe and prolonged.
  </li>
</ul>
<p><em>Action Items</em></p>
<p>
  Due to the wide-reaching nature of this incident, we split action items into five themes:
</p>
<ol type="1">
  <li>
    Prevention/risk education
  </li>
  <li>
    Emergency response
  </li>
  <li>
    Monitoring/alerting
  </li>
  <li>
    Satellite/edge provisioning
    </li>
    <li>
      Cleanup/miscellaneous
    </li>
</ol>
   <table>
      <caption class="jumptarget"><span class="label">Table 10-8. </span>Prevention/risk education</caption>
      <thead>
        <tr>
          <th>Action items</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Tracking bug</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><p>Audit all systems capable of turning live servers into paperweights (i.e., not just repairs and diskerase workflow).</p></td>
          <td><p>investigate</p></td>
          <td><p>P1</p></td>
          <td><p>sydneythree@</p></td>
          <td><p>BUG1234</p></td>
        </tr>
        <tr>
          <td><p>File bugs to track implementation of bad input rejection to all systems identified in BUG1234.</p></td>
          <td><p>prevent</p></td>
          <td><p>P1</p></td>
          <td><p>sydneythree@</p></td>
          <td><p>BUG1235</p></td>
        </tr>
        <tr>
          <td><p>Disallow any single operation from affecting servers spanning namespace/class boundaries.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P1</p></td>
          <td><p>maxone@</p></td>
          <td><p>BUG1236</p></td>
        </tr>
         <tr>
          <td><p>Traffic admin server needs a safety check to not operate on more than [value redacted] number of nodes.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P1</p></td>
          <td><p>mdylanfour@</p></td>
          <td><p>BUG1237</p></td>
        </tr>
        <tr>
          <td><p>Traffic admin server should ask &lt;safety check service&gt; to approve destructive work.</p></td>
          <td><p>prevent</p></td>
          <td><p>P0</p></td>
          <td><p>logantwo@</p></td>
          <td><p>BUG1238</p></td>
        </tr>
        <tr>
          <td><p>MDB should reject operations that do not provide values for an expected-present constraint.</p></td>
          <td><p>prevent</p></td>
          <td><p>P0</p></td>
          <td><p>louseven@</p></td>
          <td><p>BUG1239</p></td>
        </tr>
     </tbody>
    </table>
   <table>
      <caption class="jumptarget"><span class="label">Table 10-9. </span>Emergency response</caption>
      <thead>
        <tr>
          <th>Action items</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Tracking bug</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><p>Ensure that serving from core does not overload egress network links.</p></td>
          <td><p>repair</p></td>
          <td><p>P2</p></td>
          <td><p>rileysix@</p></td>
          <td><p>BUG1240</p></td>
        </tr>
        <tr>
          <td><p>Ensure decom workflow problems are noted under [the link to our emergency stop doc has been redacted] and [the link to our escalations contact page has been redacted].</p></td>
          <td><p>mitigate</p></td>
          <td><p>P2</p></td>
          <td><p>logantwo@</p></td>
          <td><p>BUG1241</p></td>
        </tr>
        <tr>
          <td><p>Add a big-red-button<sup><a class="jumptarget" data-type="noteref" id="ch10fn1-marker" href="#ch10fn1">1</a></sup> disable approach to decom workflows.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P0</p></td>
          <td><p>maxone@</p></td>
          <td><p>BUG1242</p></td>
        </tr>
     </tbody>
    </table>
   <table>
      <caption class="jumptarget"><span class="label">Table 10-10. </span>Monitoring/alerting</caption>
      <thead>
        <tr>
          <th>Action items</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Tracking bug</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><p>Monitoring target safety checks should not allow you to push a change that cannot be rolled back.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P2</p></td>
          <td><p>dylanfour@</p></td>
          <td><p>BUG1243</p></td>
        </tr>
        <tr>
          <td><p>Add an alert when more than [value redacted] % of our machines have been taken away from us. Machines were taken from satellites at 16:38 while the world started paging only at around 17:10.</p></td>
          <td><p>detect</p></td>
          <td><p>P1</p></td>
          <td><p>rileysix@</p></td>
          <td><p>BUG1244</p></td>
        </tr>
     </tbody>
    </table>
   <table>
      <caption class="jumptarget"><span class="label">Table 10-11. </span>Satellite/edge provisioning</caption>
      <thead>
        <tr>
          <th>Action items</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Tracking bug</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><p>Use iPXE to use HTTPS to make reinstalls more reliable/faster.</p></td>
          <td><p>mitigate</p></td>
          <td><p>P2</p></td>
          <td><p>dylanfour@</p></td>
          <td><p>BUG1245</p></td>
        </tr>
     </tbody>
    </table>
   <table>
      <caption class="jumptarget"><span class="label">Table 10-12. </span>Cleanup/miscellaneous</caption>
      <thead>
        <tr>
          <th>Action items</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Tracking bug</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><p>Review MDB-related code in our tools and bring the admin server backup to unwedge turnups/turndowns.</p></td>
          <td><p>repair</p></td>
          <td><p>P2</p></td>
          <td><p>rileysix@</p></td>
          <td><p>BUG1246</p></td>
        </tr>
        <tr>
          <td><p>Schedule DiRT tests:
            <ul>
              <li>
                Bring back satellite after diskerase.
              </li>
              <li>
                Do the same for YouTube CDN.
              </li>
            </ul></p></td>
          <td><p>mitigate</p></td>
          <td><p>P2</p></td>
          <td><p>louseven@</p></td>
          <td><p>BUG1247</p></td>
        </tr>
     </tbody>
    </table>
<p><em>Glossary</em></p>
<p class="italic">Admin server</p>
<ul class="simplelist">
  <li>
    An RPC server that enables automation to execute privileged operations for frontend serving infrastructure. The automation server is most visibly involved in the implementation of PCRs and cluster turnups/turndowns.
  </li>
</ul>
<p class="italic">Autoreplacer</p>
<ul class="simplelist">
  <li>
    A system that moves non-Borgified servers from machine to machine. It’s used to keep services running in the face of machine failures, and also to support forklifts and colo reconfigs.
  </li>
</ul>
<p class="italic">Borg</p>
<ul class="simplelist">
  <li>
    A cluster management system designed to manage tasks and machine resources on a massive scale. Borg owns all of the machines in a Borg cell, and assigns tasks to machines that have resources available.
  </li>
</ul>
<p class="italic">Decom</p>
<ul class="simplelist">
  <li>
    An abbreviation of <span class="italic">decommissioning</span>. Decom of equipment is a process that is relevant to many operational teams.
  </li>
</ul>
<p class="italic">Diskerase</p>
<ul class="simplelist">
  <li>
    A process (and associated hardware/software systems) to securely wipe production hard drives before they leave Google datacenters. Diskerase is a step in the decom workflow.
  </li>
</ul>
<p class="italic">GFE (Google Front End)</p>
<ul class="simplelist">
  <li>
    The server that the outside world connects to for (almost) all Google services.
  </li>
</ul>
<p class="italic">IMAG (Incident Management at Google)</p>
<ul class="simplelist">
  <li>
    A program that establishes a standard, consistent way to handle all types of incidents—from system outages to natural disasters—and organize an effective response.
  </li>
</ul>
<p class="italic">MDB (Machine Database)</p>
<ul class="simplelist">
  <li>
    A system that stores all sorts of information about the state of Google machine inventory.
  </li>
</ul>
<p class="italic">OMG (Outage Management at Google)</p>
<ul class="simplelist">
  <li>
    An incident management dashboard/tool that serves as a central place for tracking and managing all ongoing incidents at Google.
  </li>
</ul>
<p class="italic">Satellites</p>
<ul>
  <li>
    Small, inexpensive racks of machine that serve only nonvideo, frontend traffic from the edge of Google’s network. Almost none of the traditional production cluster infrastructure is available for satellites. Satellites are distinct from the CDN that serves YouTube video content from the edge of Google’s network, and from other places on the wider internet. YouTube CDN was not affected by this incident.
  </li>
</ul>
<p><em>Appendix</em></p>
<p class="italic">Why is <code><span class="italic">ReleaseSatelliteMachines</span></code> not idempotent?</p>
<ul class="simplelist">
  <li>
    [The response to this question has been elided.]
  </li>
</ul>
<p class="italic">What happened after the Admin Server assigned all satellites to the diskerase-team?</p>
<ul class="simplelist">
  <li>
    [The response to this question has been elided.]
  </li>
</ul>
<p class="italic">What was the true <a href="https://sre.google/sre-book/production-environment#xref_production-environment_job-and-data-organization">QPS</a> loss during the outage?</p>
<ul class="simplelist">
  <li>
    [The response to this question has been elided.]
  </li>
</ul>
<p class="italic">IRC logs</p>
<ul class="simplelist">
  <li>
    [The IRC logs have been elided.]
  </li>
</ul>
<p><em>Graphs</em></p>
<p class="italic">Faster latency statistics—what have satellites ever done for us?</p>
<ul class="simplelist">
  <li>
    Empirically from this outage, satellites shave [value redacted] ms latency off many locations near core clusters, and up to [value redacted] ms off locations further from our backbone:
  </li>
  <li>
    [The explanation of the graphs has been elided.]
  </li>
</ul>
<p class="italic">Core vs. Edge serving load</p>
<ul class="simplelist">
  <li>
    A nice illustration of the reconstruction effort. Being able to once again serve 50% of traffic from the edge took about 36 hours, and returning to the normal traffic balance took an additional 12 hours (see <a data-type="xref" href="#core-vs-edge-qps-breakdown">Figure 10-1</a> and <a data-type="xref" href="#core-vs-edge-qps-breakdown-alternate-representation">Figure 10-2</a>).
  </li>
</ul>
<p class="italic">Peering strain from traffic shifts</p>
<ul class="simplelist">
  <li>
    [Graph elided.]
  </li>
  <li>
    The graph shows packet loss aggregated by network region. There were a few short spikes during the event itself, but the majority of the loss occurred as various regions entered peak with little/no satellite coverage.
  </li>
</ul>
<p class="italic">Person vs. Machine, the GFE edition</p>
<ul class="simplelist">
  <li>
    [Graph explanation of human vs. automated machine setup rates elided.]
  </li>
</ul>
<figure id="core-vs-edge-qps-breakdown" class="horizontal vertical jumptarget">
      <img src="https://lh3.googleusercontent.com/L4hSmfujS0jXPgjFwTc0LdMQwLchtsPJLm86A2z6nH23ykrj0Sw39gQPtRwl37sFZ0XaZGysiBMhK6gJc1p-Pq12sDHM-fYmvSTH=s1179" alt="core-vs-edge-qps-breakdown">
      <figcaption><span class="label">Figure 10-1. </span>Core vs. Edge QPS breakdown</figcaption>
</figure>
<figure id="core-vs-edge-qps-breakdown-alternate-representation" class="horizontal vertical jumptarget">
      <img src="https://lh3.googleusercontent.com/Hqm24YUEetMrHnhfnTIyE-EG9xJ9Rz6t_Qu7qkeOc37kPVcbUfhAjyVoiK2HtWX_dZo9XXP0QOD1U33BJmFr-qKjz_xocbKfSbIAZA=s1255" alt="core-vs-edge-qps-breakdown-alternate-representation">
      <figcaption><span class="label">Figure 10-2. </span>Core vs. Edge QPS breakdown (alternate representation)</figcaption>
</figure>
</aside>

<h5 class="subheaders jumptargets" id="why-is-this-postmortem-better">Why Is This Postmortem Better?</h5>

<p>
  This postmortem exemplifies several good writing practices.
</p>

<h6 class="subheaders-small jumptargets" id="clarity">Clarity</h6>

<p>
  The postmortem is well organized and explains key terms in sufficient detail. For example:
</p>

<p class="italic">Glossary</p>

<ul class="simplelist">
  <li>
    A well-written glossary makes the postmortem accessible and comprehensible to a broad audience. 
  </li>
</ul>

<p class="italic">Action items</p>

<ul class="simplelist">
  <li>
    This was a large incident with many action items. Grouping action items by theme makes it easier to assign owners and priorities.
  </li>
</ul>

<p class="italic">Quantifiable metrics</p>

<ul class="simplelist">
  <li>
    The postmortem presents useful data on the incident, such as cache hit ratios, traffic levels, and duration of the impact. Relevant sections of the data are presented with links back to the original sources. This data transparency removes ambiguity and provides context for the reader.
  </li>
</ul>

<h6 class="subheaders-small jumptargets" id="concrete-action-items">Concrete action items</h6>

<p>
  A postmortem with no action items is ineffective. These action items have a few notable characteristics:
</p>

<p class="italic">Ownership</p>

<ul class="simplelist">
  <li>
    All action items have both an owner and a tracking number.
  </li>
</ul>

<p class="italic">Prioritization</p>

<ul class="simplelist">
  <li>
    All action items are assigned a priority level.
  </li>
</ul>

<p class="italic">Measurability</p>

<ul class="simplelist">
  <li>
    The action items have a verifiable end state (e.g., “Add an alert when more than X% of our machines have been taken away from us”).
  </li>
</ul>

<p class="italic">Preventative action</p>

<ul class="simplelist">
  <li>
    Each action item “theme” has Prevent/Mitigate action items that help avoid outage recurrence (for example, “Disallow any single operation from affecting servers spanning namespace/class boundaries”).
  </li>
</ul>

<h6 class="subheaders-small jumptargets" id="blamelessness">Blamelessness</h6>

<p>
  The authors focused on the gaps in system design that permitted undesirable failure modes. For example:
</p>

<p class="italic">Things that went poorly</p>

<ul class="simplelist">
  <li>
    No individual or team is blamed for the incident.
  </li>
</ul>

<p class="italic">Root cause and trigger</p>

<ul class="simplelist">
  <li>
    Focuses on “what” went wrong, not “who” caused the incident.
  </li>
</ul>

<p class="italic">Action items</p>

<ul class="simplelist">
  <li>
    Are aimed at improving the system instead of improving people.
  </li>
</ul>

<h6 class="subheaders-small jumptargets" id="dept">Depth</h6>

<p>
  Rather than only investigating the proximate area of the system failure, the postmortem explores the impact and system flaws across multiple teams. Specifically:
</p>

<p class="italic">Impact</p>

<ul class="simplelist">
  <li>
    This section contains lots of details from various perspectives, making it balanced and objective.
  </li>
</ul>

<p class="italic">Root cause and trigger</p>

<ul class="simplelist">
  <li>
    This section performs a deep dive on the incident and arrives at a root cause and trigger.
  </li>
</ul>

<p class="italic">Data-driven conclusions</p>

<ul class="simplelist">
  <li>
    All of the conclusions presented are based on facts and data. Any data used to arrive at a conclusion is linked from the document.
  </li>
</ul>

<p class="italic">Additional resources</p>

<ul class="simplelist">
  <li>
    These present further useful information in the form of graphs. Graphs are explained to give context to readers who aren’t familiar with the system.
  </li>
</ul>

<h6 class="subheaders-small jumptargets" id="promptness">Promptness</h6>

<p>
  The postmortem was written and circulated less than a week after the incident was closed. A prompt postmortem tends to be more accurate because information is fresh in the contributors’ minds. The people who were affected by the outage are waiting for an explanation and some demonstration that you have things under control. The longer you wait, the more they will fill the gap with the products of their imagination. That seldom works in your favor!
</p>

<h6 class="subheaders-small jumptargets" id="conciseness">Conciseness</h6>

<p>
  The incident was a global one, impacting multiple systems. As a result, the postmortem recorded and subsequently parsed a lot of data. Lengthy data sources, such as chat transcripts and system logs, were abstracted, with the unedited versions linked from the main document. Overall, the postmortem strikes a balance between verbosity and readability.
</p>

<h1 class="heading jumptargets" id="organizational-incentives">Organizational Incentives</h1>

<p>
  Ideally, senior leadership should support and encourage effective postmortems. This section describes how an organization can incentivize a healthy postmortem culture. We highlight warning signs that the culture is failing and offer some solutions. We also provide tools and templates to streamline and automate the postmortem process.
</p>

<h5 class="subheaders jumptargets" id="model-and-enforce-blameless-behavior">Model and Enforce Blameless Behavior</h5>

<p>
  To properly support postmortem culture, engineering leaders should consistently exemplify blameless behavior and encourage blamelessness in every aspect of postmortem discussion. You can use a few concrete strategies to enforce blameless behavior in an organization.
</p>

<h6 class="subheaders-small jumptargets" id="use-blameless-language">Use blameless language</h6>

<p>Blameful language stifles collaboration between teams. Consider the following scenario:</p>

<ul class="simplelist">
  <li>
    Sandy missed a service Foo training and wasn’t sure how to run a particular update command. The delay ultimately prolonged an outage.
  </li>
  <li>
    SRE Jesse [to Sandy’s manager]: “You’re the manager; why aren’t you making sure that everyone finishes the training?”
  </li>
</ul>

<p>
  The exchange includes a leading question that will instantly put the recipient on the defensive. A more balanced response would be:
</p>

<ul class="simplelist">
  <li>
    SRE Jesse [to Sandy’s manager]: “Reading the postmortem, I see that the on-caller missed an important training that would have allowed them to resolve the outage more quickly. Maybe team members should be required to complete this training before joining the on-call rotation? Or we could remind them that if they get stuck to please quickly escalate. After all, escalation is not a sin—especially if it helps lower customer pain! Long term, we shouldn't really rely so much on training, as it’s easy to forget in the heat of the moment.”
  </li>
</ul>

<h6 class="subheaders-small jumptargets" id="include-all-incident-participants-in-postmortem-authoring">Include all incident participants in postmortem authoring</h6>

<p>
  It can be easy to overlook key contributing factors to an outage when the postmortem is written in isolation or by a single team.
</p>

<h6 class="subheaders-small jumptargets" id="gather-feedback">Gather feedback</h6>

<p>
  A clear review process and communication plan for postmortems can help prevent blameful language and perspectives from propagating within an organization. For a suggested structured review process, see the section <a data-type="xref" href="#postmortem-checklist">Postmortem checklist</a>.
</p>

<h5 class="subheaders jumptargets" id="reward-postmortem-outcomes">Reward Postmortem Outcomes</h5>

<p>
  When well written, acted upon, and widely shared, postmortems are an effective vehicle for driving positive organizational change and preventing repeat outages. Consider the following strategies to incentivize postmortem culture.
</p>

<h6 class="subheaders-small jumptargets" id="reward-action-item-closeout">Reward action item closeout</h6>

<p>
  If you reward engineers for writing postmortems, but not for closing the associated action items, you risk an unvirtuous cycle of unclosed postmortems. Ensure that incentives are balanced between writing the postmortem and successfully implementing its action plan.
</p>

<h6 class="subheaders-small jumptargets" id="reward-positive-organizational-change">Reward positive organizational change</h6>

<p>
  You can incentivize widespread implementation of postmortem lessons by presenting postmortems as an opportunity to expand impact across an organization. Reward this level of impact with peer bonuses, positive performance reviews, promotion, and the like.
</p>

<h6 class="subheaders-small jumptargets" id="highlight-improved-reliability">Highlight improved reliability</h6>

<p>
  Over time, an effective postmortem culture leads to fewer outages and more reliable systems. As a result, teams can focus on feature velocity instead of infrastructure patching. It’s intrinsically motivating to highlight these improvements in reports, presentations, and performance reviews.
</p>

<h6 class="subheaders-small jumptargets" id="hold-up-postmortem-owners-as-leaders">Hold up postmortem owners as leaders</h6>

<p>
  Celebrating postmortems through emails or meetings, or by giving the authors an opportunity to present lessons learned to an audience, can appeal to individuals that appreciate public accolades. Setting up the owner as an “expert” on a type of failure and its avoidance can be rewarding for many engineers who seek peer acknowledgment. For example, you might hear someone say, “Talk to Sara, she’s an expert now. She just coauthored a postmortem where she figured out how to fix that gap!”
</p>

<h6 class="subheaders-small jumptargets" id="gamification">Gamification</h6>

<p>
  Some individuals are incentivized by a sense of accomplishment and progress toward a larger goal, such as fixing system weaknesses and increasing reliability. For these individuals, a scoreboard or burndown of postmortem action items can be an incentive. At Google, we hold “FixIt” weeks twice a year. SREs who close the most postmortem action items receive small tokens of appreciation and (of course) bragging rights. <a data-type="xref" href="#postmortem-leaderboard">Figure 10-3</a> shows an example of a postmortem leaderboard.
</p>

<figure id="postmortem-leaderboard" class="horizontal vertical jumptarget">
      <img src="https://lh3.googleusercontent.com/EiAlHicgQtGbAvCRSssHFbO2QY8A3hSyYRZMthoK6bQ_P5owLzCjMAgSoRa1ctJmX-EiOdlmSpJuAvcD_ovxPm1IRpfdwXtCOBxkgw=s1428" alt="postmortem-leaderboard">
      <figcaption><span class="label">Figure 10-3. </span>Postmortem leaderboard</figcaption>
</figure>

<h5 class="subheaders jumptargets" id="share-postmortems-openly">Share Postmortems Openly</h5>

<p>
  In order to maintain a healthy postmortem culture within an organization, it’s important to share postmortems as widely as possible. Implementing even one of the following tactics can help.
</p>

<h6 class="subheaders-small jumptargets" id="Share-announcements-across-the-organization">Share announcements across the organization</h6>

<p>
  Announce the availability of the postmortem draft on your internal communication channels, email, Slack, and the like. If you have a regular company all-hands, make it a practice to share a recent postmortem of interest.
</p>

<h6 class="subheaders-small jumptargets" id="conduct-cross-team-reviews">Conduct cross-team reviews</h6>

<p>
  Conduct cross-team reviews of postmortems. In these reviews, a team walks though their incident while other teams ask questions and learn vicariously. At Google, several offices have informal Postmortem Reading Clubs that are open to all employees.
</p>

<p>
  In addition, a cross-functional group of developers, SREs, and organizational leaders reviews the overall postmortem process. These folks meet monthly to review the effectiveness of the postmortem process and template.
</p>

<h6 class="subheaders-small jumptargets" id="hold-training-exercises">Hold training exercises</h6>

<p>
  Use the <a href="https://sre.google/sre-book/accelerating-sre-on-call#xref_training_disaster-rpg">Wheel of Misfortune</a> when training new engineers: a cast of engineers reenacts a previous postmortem, assuming roles laid out in the postmortem. The original Incident Commander attends to help make the experience as “real” as possible.
</p>

<h6 class="subheaders-small jumptargets" id="report-incidents-and-outages-weekly">Report incidents and outages weekly</h6>

<p>
  Create a weekly outage report containing the incidents and outages from the past seven days. Share the report with as wide an audience as possible. From the weekly outages, compile and share a periodic greatest hits report.
</p>

<h5 class="subheaders jumptargets" id="respond-to-postmortem-culture-failures">Respond to Postmortem Culture Failures</h5>

<p>
  The breakdown of postmortem culture may not always be obvious. The following are some common failure patterns and recommended solutions.
</p>

<h6 class="subheaders-small jumptargets" id="avoiding-association">Avoiding association</h6>

<p>
  Disengaging from the postmortem process is a sign that postmortem culture at an organization is failing. For example, suppose SRE Director Parker overhears the following conversation:
</p>

<ul class="simplelist">
  <li>
    SWE Sam: Wow, did you hear about that huge blow-up?
  </li>
  <li>
    SWE Riley: Yeah, it was terrible. They’ll have to write a postmortem now.
  </li>
  <li>
    SWE Sam: Oh no! I’m so glad I’m not involved with that.
  </li>
  <li>
    SWE Riley: Yeah, I really wouldn’t want to be in the meeting where that one is discussed.
  </li>
</ul>

<p>
  Ensuring that high-visibility postmortems are <a data-type="xref" href="#postmortem-checklist">reviewed</a> for blameful prose can help prevent this kind of avoidance. In addition, sharing high-quality examples and discussing how those involved were rewarded can help reengage individuals.
</p>

<h6 class="subheaders-small jumptargets" id="failing-to-reinforce-the-culture">Failing to reinforce the culture</h6>

<p>
  Responding when a senior executive uses blameful language can be challenging. Consider the following statement made by senior leadership at a meeting about an outage:
</p>

<ul class="simplelist">
  <li>VP Ash: I know we are supposed to be blameless, but this is a safe space. Someone must have known beforehand this was a bad idea, so why didn’t you listen to that person?</li>
</ul>

<p>Mitigate the damage by moving the narrative in a more constructive direction. For example:
</p>

<ul class="simplelist">
  <li>
    SRE Dana: Hmmm, I’m sure everyone had the best intent, so to keep it blameless, maybe we ask generically if there were any warning signs we could have heeded, and why we might have dismissed them.
  </li>
</ul>

<p>
  Individuals act in good faith and make decisions based on the best information available. Investigating the source of misleading information is much more beneficial to the organization than assigning blame. (If you have encountered Agile principles, this should <a href="https://martinfowler.com/bliki/PrimingPrimeDirective.html" target="_blank" rel="noopener noreferrer">be familiar to you</a>.)
</p>

<h6 class="subheaders-small jumptargets" id="lacking-time-to-write-postmortems">Lacking time to write postmortems</h6>

<p>
  Quality postmortems take time to write. When a team is overloaded with other tasks, the quality of postmortems suffers. Subpar postmortems with incomplete action items make a recurrence far more likely. Postmortems are letters you write to future team members: it’s very important to keep a consistent quality bar, lest you accidentally teach future teammates a bad lesson. Prioritize postmortem work, track the postmortem completion and review, and allow teams adequate time to implement the associated action plan. The tooling we discuss in the section <a data-type="xref" href="#tools-and-templates">Tools and Templates</a> can help with these activities.
</p>

<h6 class="subheaders-small jumptargets" id="repeating-incidents">Repeating incidents</h6>

<p>
  If teams are experiencing failures that mirror previous incidents, it’s time to dig deeper. Consider asking questions like:
</p>

<ul>
  <li>
    Are action items taking too long to close?
  </li>
  <li>
    Is feature velocity trumping reliability fixes?
  </li>
  <li>
    Are the right action items being captured in the first place?
  </li>
  <li>
    Is the faulty service overdue for a refactor?
  </li>
  <li>
    Are people putting Band-Aids on a more serious problem?
  </li>
</ul>

<p>
  If you uncovered a systemic process or technical problem, it’s time to take a step back and consider the overall service health. Bring the postmortem collaborators from each similar incident together to discuss the best course of action to prevent repeats.
</p>

<h1 class="heading jumptargets" id="tools-and-templates">Tools and Templates</h1>

<p>
  A set of tools and templates can bootstrap a postmortem culture by making writing postmortems and managing the associated data easier. There are a number of resources from Google and other companies that you can leverage in this space.
</p>

<h5 class="subheaders jumptargets" id="postmortem-templates">Postmortem Templates</h5>

<p>
  Templates make it easier to write complete postmortems and share them across an organization. Using a standard format makes postmortems more accessible for readers outside the domain. You can customize the template to fit your needs. For example, it may be useful to capture team-specific metadata like hardware make/model for a datacenter team, or Android versions affected for a mobile team. You can then add customizations as the team matures and performs more sophisticated postmortems.
</p>

<h6 class="subheaders-small jumptargets" id="googles-template">Google’s template</h6>

<p>
  Google has shared a version of our postmortem template in Google Docs format at <a href="https://drive.google.com/corp/drive/folders/1t7fO8M3EZFeuu4GmzvStd0TGDI4bDCeb" target="_blank" rel="noopener noreferrer"><span class="italic">https://g.co/SiteReliabilityWorkbookMaterials</span></a>. Internally, we primarily use Docs to write postmortems because it facilitates collaboration via shared editing rights and comments. Some of our internal tools prepopulate this template with metadata to make the postmortem easier to write. We leverage <a href="https://developers.google.com/apps-script/" target="_blank" rel="noopener noreferrer">Google Apps Script</a> to automate parts of the authoring, and capture a lot of the data into specific sections and tables to make it easier for our postmortem repository to parse out data for analysis.
</p>

<h6 class="subheaders-small jumptargets" id="other-industry-templates">Other industry templates</h6>

<p>Several other companies and individuals have shared their postmortem templates:</p>

<ul>
  <li>
    <a href="https://response.pagerduty.com/after/post_mortem_template/" target="_blank" rel="noopener noreferrer">Pager Duty</a>
  </li>
  <li>
    <a href="https://gist.github.com/mlafeldt/6e02ea0caeebef1205b47f31c2647966" target="_blank" rel="noopener noreferrer">An adaptation of the original Google Site Reliability Engineering book template</a>
  </li>
  <li>
    <a href="https://github.com/dastergon/postmortem-templates/tree/master/templates" target="_blank" rel="noopener noreferrer">A list of four templates hosted on GitHub</a>
  </li>
  <li>
    <a href="https://gist.github.com/juliandunn/52b4fbde451628e0fe48" target="_blank" rel="noopener noreferrer">GitHub user Julian Dunn</a>
  </li>
  <li>
    <a href="https://serverfault.com/questions/29188/documenting-an-outage-for-a-post-mortem-review" target="_blank" rel="noopener noreferrer">Server Fault</a>
  </li>
</ul>

<h5 class="subheaders jumptargets" id="postmortem-tooling">Postmortem Tooling</h5>

<p>
  As of this writing, Google’s postmortem management tooling is not available for external use (check our <a href="https://cloud.google.com/blog/" target="_blank" rel="noopener noreferrer">blog</a> for the latest updates). We can, however, explain how our tools facilitate postmortem culture.
</p>

<h6 class="subheaders-small jumptargets" id="postmortem-creation">Postmortem creation</h6>

<p>Our incident management tooling collects and stores a lot of useful data about an incident and pushes that data automatically into the postmortem. Examples of data we push includes:</p>

<ul>
  <li>
    Incident Commander and other roles
  </li>
  <li>
    Detailed incident timeline and IRC logs
  </li>
  <li>
    Services affected and root-cause services
  </li>
  <li>
    Incident severity
  </li>
  <li>
    Incident detection mechanisms
  </li>
</ul>

<h6 class="subheaders-small jumptargets" id="postmortem-checklist">Postmortem checklist</h6>

<p>
  To help authors ensure a postmortem is properly completed, we provide a postmortem checklist that walks the owner through key steps. Here are just a few example checks on the list:
</p>

<ul>
  <li>
    Perform a complete assessment of incident impact.
  </li>
  <li>
    Conduct sufficiently detailed root-cause analysis to drive action item planning.
  </li>
  <li>
    Ensure action items are vetted and approved by the technical leads of the service.
  </li>
  <li>
    Share the postmortem with the wider organization.
  </li>
</ul>

<p>The full checklist is available at <a href="https://drive.google.com/corp/drive/folders/1t7fO8M3EZFeuu4GmzvStd0TGDI4bDCeb" target="_blank" rel="noopener noreferrer"><span class="italic">https://g.co/SiteReliabilityWorkbookMaterials</span></a>.</p>

<h6 class="subheaders-small jumptargets" id="postmortem-storage">Postmortem storage</h6>

<p>
  We store postmortems in a tool called Requiem so it’s easy for any Googler to find them. Our incident management tool automatically pushes all postmortems to Requiem, and anyone in the organization can post their postmortem for all to see. We have thousands of postmortems stored, dating back to 2009. Requiem parses out metadata from individual postmortems and makes it available for searching, analysis, and reporting.
</p>

<h6 class="subheaders-small jumptargets" id="postmortem-follow-up">Postmortem follow-up</h6>

<p>
  Our postmortems are stored in Requiem’s database. Any resulting action items are filed as bugs in our centralized bug tracking system. Consequently, we can monitor the closure of action items from each postmortem. With this level of tracking, we can ensure that action items don’t slip through the cracks, leading to increasingly unstable services. <a data-type="xref" href="#postmortem-action-item-monitoring">Figure 10-4</a> shows a mockup of postmortem action item monitoring enabled by our tooling.
</p>

<figure id="postmortem-action-item-monitoring" class="horizontal vertical jumptarget">
      <img src="https://lh3.googleusercontent.com/xLWW2u96whkMS7IRm5vBxGFLlDZufrMG_e_K_Cae_lzmKubOb2m73d-8W7my1IsF8WHVDD7Fo9YtuHUkL0UpEXn3D5_tDOaocuUjHg=s1108" alt="postmortem-action-item-monitoring">
      <figcaption><span class="label">Figure 10-4. </span>Postmortem action item monitoring</figcaption>
</figure>

<h6 class="subheaders-small jumptargets" id="postmortem-analysis">Postmortem analysis</h6>

<p>
  Our postmortem management tool stores its information in a database for analysis. Teams can use the data to write reports about their postmortem trends and identify their most vulnerable systems. This helps us uncover underlying sources of instability or incident management dysfunctions that may otherwise go unnoticed. For example, <a data-type="xref" href="#postmortem-analysis">Figure 10-5</a> shows charts that were built with our analysis tooling. These charts show us trends like how many postmortems we have per month per organization, incident mean duration, time to detect, time to resolve, and blast radius.
</p>

<aside data-type="sidebar" class="highlight pagebreak-before note-highlight">
<h6 class="subheaders-small jumptargets" id="note-3" align="center">Note</h6>
<h6 class="subheaders-small note jumptargets" id="a-simple-way-to-get-started"><em>A simple way to get started</em></h6>
<p class="note">
We have provided a simple postmortem template and sheet with some Apps Scripts that will parse metadata from postmortems using the template. Use these tools to experiment with rudimentary postmortem indexing and analysis.
</p>
</aside>

<figure id="postmortem-analysis" class="horizontal vertical jumptarget">
      <img src="https://lh3.googleusercontent.com/J-lGz60sgLQEJN2xl-sKmYpZVpgI67Hn9aFLl1X_xzozPncmiAmnDROwNBayMkpj3x5wJR_H-Htpzs9KAIbaLaA8Zew1ROWQiTpePB4=s997" alt="postmortem-analysis">
      <figcaption><span class="label">Figure 10-5. </span>Postmortem analysis</figcaption>
</figure>

<h6 class="subheaders-small jumptargets" id="other-industry-tools">Other industry tools</h6>

<p>Here are some third-party tools that can help you create, organize, and analyze postmortems:</p>

<ul>
  <li>
    <a href="https://www.pagerduty.com/features/post-mortems/" target="_blank" rel="noopener noreferrer">Pager Duty Postmortems</a>
  </li>
  <li>
    <a href="https://github.com/etsy/morgue" target="_blank" rel="noopener noreferrer">Morgue by Etsy</a>
  </li>
  <li>
    <a href="https://victorops.com/blog/importance-of-post-mortems" target="_blank" rel="noopener noreferrer">VictorOps</a>
  </li>
</ul>

<p>
  Although it’s impossible to fully automate every step of writing postmortems, we’ve found that postmortem templates and tooling make the process run more smoothly. These tools free up time, allowing authors to focus on the critical aspects of the postmortem, such as root-cause analysis and action item planning.
</p>

<h1 class="heading jumptargets" id="conclusion">Conclusion</h1>

<p>
  Ongoing investment in cultivating a postmortem culture pays dividends in the form of fewer outages, a better overall experience for users, and more trust from the people that depend on you. Consistent application of these practices results in better system design, less downtime, and more effective and happier engineers. If the worst does happen and an incident recurs, you will suffer less damage and recover faster and have even more data to continue reinforcing production.
</p>

<div data-type="footnotes" class="footnotes">
  <p data-type="footnote" id="ch10fn1"><sup><a class="jumptargets" href="#ch10fn1-marker">1</a></sup>A general term for a shut-down switch (e.g., an emergency power-off button) to be used in catastrophic circumstances to avert further damage.
  </p>
</div>
    </div>
  </div>

  <div class="footer">
    <div class="maia-aux">
      <div class="previous">
          <a href="/workbook/incident-response/">
            <p class="footer-caption">Previous</p>
            <p class="chapter-link">
                Chapter 9 - Incident Response
            </p>
          </a>
      </div>
      <div class="next">
          <a href="/workbook/managing-load/">
            <p class="footer-caption">Next</p>
            <p class="chapter-link">
                Chapter 11 - Managing Load
            </p>
          </a>
      </div>
        <p class="footer-link">Copyright © 2018 Google, Inc. Published by O'Reilly Media, Inc. Licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" rel="noopener noreferrer" target="_blank">CC BY-NC-ND 4.0</a></p>
    </div>
  </div>
    </main>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.6.6/angular.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.6.6/angular-animate.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.6.6/angular-touch.min.js"></script>
    <script src="/sre-book/static/js/index.min.js?cache=5b7f90b"></script>

  </body>
</html>