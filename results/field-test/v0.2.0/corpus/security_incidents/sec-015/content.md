<!DOCTYPE html>
<html>
<head> <title>curl - CVEs</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
<link rel="stylesheet" type="text/css" href="/curl.css">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="icon" href="/logo/curl-symbol.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="curl Releases" href="https://github.com/curl/curl/releases.atom">
<style type="text/css">
.contents {
  max-width: 70%;
  overflow: auto;
}
</style>
</head>
<body>
<div class="main">
<nav class="sitenav" aria-label="Primary navigation">
<a class="curlsymbol sitenav-home" href="/" aria-label="curl home">
  <img src="/logo/curl-white-symbol.svg" alt="">
</a>
<input class="sitenav-state" type="checkbox" id="sitenav-state"> <label class="sitenav-toggle" for="sitenav-state">  <span class="sitenav-toggle-icon" aria-hidden="true"></span>  <span>Menu</span> </label>
<ul class="sitenav-list">
<li class="sitenav-item"><a class="sitenav-link menuitem" href="/docs/" title="Documentation Overview">Docs Overview</a></li>
<li class="sitenav-item">  <details class="sitenav-disclosure" name="sitenav-submenus">  <summary class="sitenav-summary">  <span class="sitenav-label">Project</span>  </summary>  <ul class="sitenav-submenu">
  <li><a class="sitenav-overview" href="/docs/projdocs.html">Project overview</a></li>
  <li><a href="/docs/bugs.html">Bug Report</a></li>
  <li><a href="/docs/code-of-conduct.html">Code of conduct</a></li>
  <li><a href="/docs/libs.html">Dependencies</a></li>
  <li><a href="/donation.html">Donate</a></li>
  <li><a href="/docs/faq.html">FAQ</a></li>
  <li><a href="/docs/features.html">Features</a></li>
  <li><a href="/docs/governance.html">Governance</a></li>
  <li><a href="/docs/history.html">History</a></li>
  <li><a href="/docs/install.html">Install</a></li>
  <li><a href="/docs/knownbugs.html">Known Bugs</a></li>
  <li><a href="/docs/knownrisks.html">Known Risks</a></li>
  <li><a href="/logo/">Logo</a></li>
  <li><a href="/docs/todo.html">TODO</a></li>
  <li><a href="/about.html">website Info</a></li>
</ul>  </details> </li>
<li class="sitenav-item">  <details class="sitenav-disclosure" name="sitenav-submenus">  <summary class="sitenav-summary">  <span class="sitenav-label">Protocols</span>  </summary>  <ul class="sitenav-submenu">
  <li><a class="sitenav-overview" href="/docs/protdocs.html">Protocols overview</a></li>
  <li><a href="/docs/caextract.html">CA Extract</a></li>
  <li><a href="/docs/http-cookies.html">HTTP cookies</a></li>
  <li><a href="/docs/http3.html">HTTP/3</a></li>
  <li><a href="/docs/mqtt.html">MQTT</a></li>
  <li><a href="/docs/sslcerts.html">SSL certs</a></li>
  <li><a href="/docs/ssl-compared.html">SSL libs compared</a></li>
  <li><a href="/docs/url-syntax.html">URL syntax</a></li>
  <li><a href="/docs/websocket.html">WebSocket</a></li>
</ul>  </details> </li>
<li class="sitenav-item">  <details class="sitenav-disclosure" name="sitenav-submenus">  <summary class="sitenav-summary">  <span class="sitenav-label">Releases</span>  </summary>  <ul class="sitenav-submenu">
  <li><a class="sitenav-overview" href="/docs/reldocs.html">Releases overview</a></li>
  <li><a href="/ch/">Changelog</a></li>
  <li><a href="/docs/releases.html">Release Table</a></li>
  <li><a href="/docs/versions.html">Version Numbering</a></li>
  <li><a href="/docs/verify.html">Verify</a></li>
</ul>  </details> </li>
<li class="sitenav-item">  <details class="sitenav-disclosure" name="sitenav-submenus">  <summary class="sitenav-summary">  <span class="sitenav-label">Security</span>  </summary>  <ul class="sitenav-submenu">
  <li><a class="sitenav-overview" href="/docs/secdocs.html">Security overview</a></li>
  <li><a href="/docs/audits.html">Security Audits</a></li>
  <li><a href="/docs/security.html">curl CVEs</a></li>
  <li><a href="/dev/advisory.html">Security advisory details</a></li>
  <li><a href="/docs/vulnerabilities.html">Vulnerability table</a></li>
  <li><a href="/dev/vuln-disclosure.html">Vulnerability Disclosure Policy</a></li>
</ul>  </details> </li>
<li class="sitenav-item">  <details class="sitenav-disclosure" name="sitenav-submenus">  <summary class="sitenav-summary">  <span class="sitenav-label">Tool</span>  </summary>  <ul class="sitenav-submenu">
  <li><a class="sitenav-overview" href="/docs/tooldocs.html">Tool overview</a></li>
  <li><a href="/docs/comparison-table.html">Comparison Table</a></li>
  <li><a href="/docs/manpage.html">curl man page</a></li>
  <li><a href="/docs/httpscripting.html">HTTP Scripting</a></li>
  <li><a href="/docs/mk-ca-bundle.html">mk-ca-bundle</a></li>
  <li><a href="/docs/tutorial.html">Tutorial</a></li>
  <li><a href="/docs/optionswhen.html">When options were added</a></li>
</ul>  </details> </li>
<li class="sitenav-item">  <details class="sitenav-disclosure" name="sitenav-submenus">  <summary class="sitenav-summary">  <span class="sitenav-label">Who and Why</span>  </summary>  <ul class="sitenav-submenu">
  <li><a class="sitenav-overview" href="/docs/whodocs.html">Who and Why overview</a></li>
  <li><a href="/docs/companies.html">Companies</a></li>
  <li><a href="/docs/copyright.html">Copyright</a></li>
  <li><a href="/sponsors.html">Sponsors</a></li>
  <li><a href="/docs/thanks.html">Thanks</a></li>
  <li><a href="/docs/thename.html">The name</a></li>
</ul>  </details> </li>
</ul>
</nav>
<div class="contents">
<div class="where"><a href="/">curl</a> / <a href="/docs/">Docs</a> / <a href="/docs/reldocs.html">Releases</a> / <b>curl CVEs</b></div>
<h1> curl CVEs </h1>
<div class="relatedbox">
<b>Related:</b>
<br><a href="audits.html">Audits</a>
<br><a href="/ch/">Changelog</a>
<br><a href="security.html">curl CVEs</a>
<br><a href="/dev/vuln-disclosure.html">Vulnerability Disclosure</a>
<br><a href="vulnerabilities.html">Vulnerabilities Table</a>
</div>
<p>
 If you find or suspect a security problem in curl or libcurl, please
 file <a href="/dev/vuln-disclosure.html">a detailed report</a> to us.
<p>
 See also the <a href="vulnerabilities.html">Vulnerabilities Table</a> to see
 what versions that are vulnerable to what flaws.
<h2> Published vulnerabilities for curl/libcurl </h2>
<a href="security.html">All</a> |
<a href="security-m.html">Medium+</a> |
<a href="security-h.html">High+</a> |
<a href="security-c.html">Critical</a>
<p>
(The table below shows vulnerabilities of all severity levels)
<table>
<tr class="tabletop">
<th title="Vulnerability number">#</th>
<th title="Severity: L=Low, M=Medium, H=High, C=Critical">S</th>
<th title="Where: Tool-only, Lib-only, default means both">W</th>
<th title="C mistake or not">C</th>
<th>Vulnerability</th>
<th title="Date publicly disclosed">Published</th>
<th title="First curl version affected">First</th>
<th title="Last curl version affected">Last</th>
<th title="Bug-bounty award">Awarded</th>
</tr>
<tr>
<td>206</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2026-12064.html">CVE-2026-12064: proto-default skips SSH verification</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.81.0.html">7.81.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>205</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-11856.html">CVE-2026-11856: cross-origin Digest auth state leak</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>204</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-11586.html">CVE-2026-11586: WS Auto-PONG memory exhaustion</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.16.0.html">8.16.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>203</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-11564.html">CVE-2026-11564: Native CA trust persist</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>202</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-11352.html">CVE-2026-11352: QUIC zero-length UDP datagrams busy-loop</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.18.0.html">8.18.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>201</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2026-10536.html">CVE-2026-10536: HTTP/2 stream-dependency tree UAF</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.88.0.html">7.88.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>200</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-9547.html">CVE-2026-9547: SSH improper host validation</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.69.0.html">7.69.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>199</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-9546.html">CVE-2026-9546: sending old referer</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.18.0.html">8.18.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>198</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-9545.html">CVE-2026-9545: exposing HTTP/3 early data</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.11.0.html">8.11.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>197</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2026-9080.html">CVE-2026-9080: UAF after pause in socket callback</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.13.0.html">8.13.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>196</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-9079.html">CVE-2026-9079: stale proxy password leak</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.8.0.html">8.8.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>195</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-8932.html">CVE-2026-8932: incomplete mTLS config matching in conn reuse</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>194</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-8927.html">CVE-2026-8927: env-set cross-proxy Digest auth state leak</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.12.0.html">7.12.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>193</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-8926.html">CVE-2026-8926: password leak with netrc and user in URL</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.11.1.html">8.11.1</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>192</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2026-8925.html">CVE-2026-8925: SASL double-free</a></td>
<td>2026-06-24</td>
<td><a href="vuln-8.15.0.html">8.15.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>191</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-8924.html">CVE-2026-8924: trailing dot domain super cookie</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.46.0.html">7.46.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>190</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-8458.html">CVE-2026-8458: wrong reuse for different services</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.43.0.html">7.43.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>189</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-8286.html">CVE-2026-8286: wrong STARTTLS connection reuse</a></td>
<td>2026-06-24</td>
<td><a href="vuln-7.30.0.html">7.30.0</a></td>
<td><a href="vuln-8.20.0.html">8.20.0</a></td>
<td></td>
</tr>
<tr>
<td>188</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-7168.html">CVE-2026-7168: cross-proxy Digest auth state leak</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.12.0.html">7.12.0</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>187</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-7009.html">CVE-2026-7009: OCSP stapling bypass with Apple SecTrust</a></td>
<td>2026-04-29</td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>186</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-6429.html">CVE-2026-6429: netrc credential leak with reused proxy connection</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.14.0.html">7.14.0</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>185</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2026-6276.html">CVE-2026-6276: stale custom cookie host causes cookie leak</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.71.0.html">7.71.0</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>184</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-6253.html">CVE-2026-6253: proxy credentials leak over redirect-to proxy</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.14.1.html">7.14.1</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>183</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-5773.html">CVE-2026-5773: wrong reuse of SMB connection</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.40.0.html">7.40.0</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>182</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-5545.html">CVE-2026-5545: wrong reuse of HTTP Negotiate connection</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>181</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-4873.html">CVE-2026-4873: connection reuse ignores TLS requirement</a></td>
<td>2026-04-29</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-8.19.0.html">8.19.0</a></td>
<td></td>
</tr>
<tr>
<td>180</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2026-3805.html">CVE-2026-3805: use after free in SMB connection reuse</a></td>
<td>2026-03-11</td>
<td><a href="vuln-8.13.0.html">8.13.0</a></td>
<td><a href="vuln-8.18.0.html">8.18.0</a></td>
<td></td>
</tr>
<tr>
<td>179</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-3784.html">CVE-2026-3784: wrong proxy connection reuse with credentials</a></td>
<td>2026-03-11</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-8.18.0.html">8.18.0</a></td>
<td></td>
</tr>
<tr>
<td>178</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-3783.html">CVE-2026-3783: token leak with redirect and netrc</a></td>
<td>2026-03-11</td>
<td><a href="vuln-7.33.0.html">7.33.0</a></td>
<td><a href="vuln-8.18.0.html">8.18.0</a></td>
<td></td>
</tr>
<tr>
<td>177</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2026-1965.html">CVE-2026-1965: bad reuse of HTTP Negotiate connection</a></td>
<td>2026-03-11</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-8.18.0.html">8.18.0</a></td>
<td></td>
</tr>
<tr>
<td>176</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-15224.html">CVE-2025-15224: libssh key passphrase bypass without agent set</a></td>
<td>2026-01-07</td>
<td><a href="vuln-7.58.0.html">7.58.0</a></td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>175</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-15079.html">CVE-2025-15079: libssh global known_hosts override</a></td>
<td>2026-01-07</td>
<td><a href="vuln-7.58.0.html">7.58.0</a></td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>174</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2025-14819.html">CVE-2025-14819: OpenSSL partial chain store policy bypass</a></td>
<td>2026-01-07</td>
<td><a href="vuln-7.87.0.html">7.87.0</a></td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>173</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-14524.html">CVE-2025-14524: bearer token leak on cross-protocol redirect</a></td>
<td>2026-01-07</td>
<td><a href="vuln-7.33.0.html">7.33.0</a></td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>172</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2025-14017.html">CVE-2025-14017: broken TLS options for threaded LDAPS</a></td>
<td>2026-01-07</td>
<td><a href="vuln-7.17.0.html">7.17.0</a></td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>171</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-13034.html">CVE-2025-13034: No QUIC certificate pinning with GnuTLS</a></td>
<td>2026-01-07</td>
<td><a href="vuln-8.8.0.html">8.8.0</a></td>
<td><a href="vuln-8.17.0.html">8.17.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>170</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-10966.html">CVE-2025-10966: missing SFTP host verification with wolfSSH</a></td>
<td>2025-11-05</td>
<td><a href="vuln-7.69.0.html">7.69.0</a></td>
<td><a href="vuln-8.16.0.html">8.16.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>169</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-10148.html">CVE-2025-10148: predictable WebSocket mask</a></td>
<td>2025-09-10</td>
<td><a href="vuln-8.11.0.html">8.11.0</a></td>
<td><a href="vuln-8.15.0.html">8.15.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>168</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2025-9086.html">CVE-2025-9086: Out of bounds read for cookie path</a></td>
<td>2025-09-10</td>
<td><a href="vuln-8.13.0.html">8.13.0</a></td>
<td><a href="vuln-8.15.0.html">8.15.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>167</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2025-5399.html">CVE-2025-5399: WebSocket endless loop</a></td>
<td>2025-06-04</td>
<td><a href="vuln-8.13.0.html">8.13.0</a></td>
<td><a href="vuln-8.14.0.html">8.14.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>166</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-5025.html">CVE-2025-5025: No QUIC certificate pinning with wolfSSL</a></td>
<td>2025-05-28</td>
<td><a href="vuln-8.5.0.html">8.5.0</a></td>
<td><a href="vuln-8.13.0.html">8.13.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>165</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-4947.html">CVE-2025-4947: QUIC certificate check skip with wolfSSL</a></td>
<td>2025-05-28</td>
<td><a href="vuln-8.8.0.html">8.8.0</a></td>
<td><a href="vuln-8.13.0.html">8.13.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>164</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2025-0725.html">CVE-2025-0725: gzip integer overflow</a></td>
<td>2025-02-05</td>
<td><a href="vuln-7.10.5.html">7.10.5</a></td>
<td><a href="vuln-8.11.1.html">8.11.1</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>163</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-0665.html">CVE-2025-0665: eventfd double close</a></td>
<td>2025-02-05</td>
<td><a href="vuln-8.11.1.html">8.11.1</a></td>
<td><a href="vuln-8.11.1.html">8.11.1</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>162</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2025-0167.html">CVE-2025-0167: netrc and default credential leak</a></td>
<td>2025-02-05</td>
<td><a href="vuln-7.76.0.html">7.76.0</a></td>
<td><a href="vuln-8.11.1.html">8.11.1</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>161</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-11053.html">CVE-2024-11053: netrc and redirect credential leak</a></td>
<td>2024-12-11</td>
<td><a href="vuln-7.76.0.html">7.76.0</a></td>
<td><a href="vuln-8.11.0.html">8.11.0</a></td>
<td>505 USD</td>
</tr>
<tr>
<td>160</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-9681.html">CVE-2024-9681: HSTS subdomain overwrites parent cache entry</a></td>
<td>2024-11-06</td>
<td><a href="vuln-7.74.0.html">7.74.0</a></td>
<td><a href="vuln-8.10.1.html">8.10.1</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>159</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-8096.html">CVE-2024-8096: OCSP stapling bypass with GnuTLS</a></td>
<td>2024-09-11</td>
<td><a href="vuln-7.41.0.html">7.41.0</a></td>
<td><a href="vuln-8.9.1.html">8.9.1</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>158</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2024-7264.html">CVE-2024-7264: ASN.1 date parser overread</a></td>
<td>2024-07-31</td>
<td><a href="vuln-7.32.0.html">7.32.0</a></td>
<td><a href="vuln-8.9.0.html">8.9.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>157</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2024-6874.html">CVE-2024-6874: macidn punycode buffer overread</a></td>
<td>2024-07-24</td>
<td><a href="vuln-8.8.0.html">8.8.0</a></td>
<td><a href="vuln-8.8.0.html">8.8.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>156</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: BAD_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2024-6197.html">CVE-2024-6197: freeing stack buffer in utf8asn1str</a></td>
<td>2024-07-24</td>
<td><a href="vuln-8.6.0.html">8.6.0</a></td>
<td><a href="vuln-8.8.0.html">8.8.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>155</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-2466.html">CVE-2024-2466: TLS certificate check bypass with mbedTLS</a></td>
<td>2024-03-27</td>
<td><a href="vuln-8.5.0.html">8.5.0</a></td>
<td><a href="vuln-8.6.0.html">8.6.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>154</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2024-2398.html">CVE-2024-2398: HTTP/2 push headers memory-leak</a></td>
<td>2024-03-27</td>
<td><a href="vuln-7.44.0.html">7.44.0</a></td>
<td><a href="vuln-8.6.0.html">8.6.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>153</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-2379.html">CVE-2024-2379: QUIC certificate check bypass with wolfSSL</a></td>
<td>2024-03-27</td>
<td><a href="vuln-8.6.0.html">8.6.0</a></td>
<td><a href="vuln-8.6.0.html">8.6.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>152</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-2004.html">CVE-2024-2004: Usage of disabled protocol</a></td>
<td>2024-03-27</td>
<td><a href="vuln-7.85.0.html">7.85.0</a></td>
<td><a href="vuln-8.6.0.html">8.6.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>151</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2024-0853.html">CVE-2024-0853: OCSP verification bypass with TLS session reuse</a></td>
<td>2024-01-31</td>
<td><a href="vuln-8.5.0.html">8.5.0</a></td>
<td><a href="vuln-8.5.0.html">8.5.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>150</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-46219.html">CVE-2023-46219: HSTS long filename clears contents</a></td>
<td>2023-12-06</td>
<td><a href="vuln-7.84.0.html">7.84.0</a></td>
<td><a href="vuln-8.4.0.html">8.4.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>149</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-46218.html">CVE-2023-46218: cookie mixed case PSL bypass</a></td>
<td>2023-12-06</td>
<td><a href="vuln-7.46.0.html">7.46.0</a></td>
<td><a href="vuln-8.4.0.html">8.4.0</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>148</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2023-38546.html">CVE-2023-38546: cookie injection with none file</a></td>
<td>2023-10-11</td>
<td><a href="vuln-7.9.1.html">7.9.1</a></td>
<td><a href="vuln-8.3.0.html">8.3.0</a></td>
<td>540 USD</td>
</tr>
<tr>
<td>147</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2023-38545.html">CVE-2023-38545: SOCKS5 heap buffer overflow</a></td>
<td>2023-10-11</td>
<td><a href="vuln-7.69.0.html">7.69.0</a></td>
<td><a href="vuln-8.3.0.html">8.3.0</a></td>
<td>4660 USD</td>
</tr>
<tr>
<td>146</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-38039.html">CVE-2023-38039: HTTP headers eat all memory</a></td>
<td>2023-09-13</td>
<td><a href="vuln-7.84.0.html">7.84.0</a></td>
<td><a href="vuln-8.2.1.html">8.2.1</a></td>
<td>2540 USD</td>
</tr>
<tr>
<td>145</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2023-28322.html">CVE-2023-28322: more POST-after-PUT confusion</a></td>
<td>2023-05-17</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-8.0.1.html">8.0.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>144</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-28321.html">CVE-2023-28321: IDN wildcard match</a></td>
<td>2023-05-17</td>
<td><a href="vuln-7.12.0.html">7.12.0</a></td>
<td><a href="vuln-8.0.1.html">8.0.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>143</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2023-28320.html">CVE-2023-28320: siglongjmp race condition</a></td>
<td>2023-05-17</td>
<td><a href="vuln-7.9.8.html">7.9.8</a></td>
<td><a href="vuln-8.0.1.html">8.0.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>142</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2023-28319.html">CVE-2023-28319: UAF in SSH sha256 fingerprint check</a></td>
<td>2023-05-17</td>
<td><a href="vuln-7.81.0.html">7.81.0</a></td>
<td><a href="vuln-8.0.1.html">8.0.1</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>141</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-27538.html">CVE-2023-27538: SSH connection too eager reuse still</a></td>
<td>2023-03-20</td>
<td><a href="vuln-7.16.1.html">7.16.1</a></td>
<td><a href="vuln-7.88.1.html">7.88.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>140</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2023-27537.html">CVE-2023-27537: HSTS double free</a></td>
<td>2023-03-20</td>
<td><a href="vuln-7.88.0.html">7.88.0</a></td>
<td><a href="vuln-7.88.1.html">7.88.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>139</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2023-27536.html">CVE-2023-27536: GSS delegation too eager connection reuse</a></td>
<td>2023-03-20</td>
<td><a href="vuln-7.22.0.html">7.22.0</a></td>
<td><a href="vuln-7.88.1.html">7.88.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>138</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-27535.html">CVE-2023-27535: FTP too eager connection reuse</a></td>
<td>2023-03-20</td>
<td><a href="vuln-7.13.0.html">7.13.0</a></td>
<td><a href="vuln-7.88.1.html">7.88.1</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>137</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-27534.html">CVE-2023-27534: SFTP path ~ resolving discrepancy</a></td>
<td>2023-03-20</td>
<td><a href="vuln-7.18.0.html">7.18.0</a></td>
<td><a href="vuln-7.88.1.html">7.88.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>136</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-27533.html">CVE-2023-27533: TELNET option IAC injection</a></td>
<td>2023-03-20</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.88.1.html">7.88.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>135</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-23916.html">CVE-2023-23916: HTTP multi-header compression denial of service</a></td>
<td>2023-02-15</td>
<td><a href="vuln-7.57.0.html">7.57.0</a></td>
<td><a href="vuln-7.87.0.html">7.87.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>134</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-23915.html">CVE-2023-23915: HSTS amnesia with --parallel</a></td>
<td>2023-02-15</td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td><a href="vuln-7.87.0.html">7.87.0</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>133</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2023-23914.html">CVE-2023-23914: HSTS ignored on multiple requests</a></td>
<td>2023-02-15</td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td><a href="vuln-7.87.0.html">7.87.0</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>132</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2022-43552.html">CVE-2022-43552: HTTP Proxy deny use after free</a></td>
<td>2022-12-21</td>
<td><a href="vuln-7.16.0.html">7.16.0</a></td>
<td><a href="vuln-7.86.0.html">7.86.0</a></td>
<td></td>
</tr>
<tr>
<td>131</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-43551.html">CVE-2022-43551: Another HSTS bypass via IDN</a></td>
<td>2022-12-21</td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td><a href="vuln-7.86.0.html">7.86.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>130</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-42916.html">CVE-2022-42916: HSTS bypass via IDN</a></td>
<td>2022-10-26</td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td><a href="vuln-7.85.0.html">7.85.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>129</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2022-42915.html">CVE-2022-42915: HTTP proxy double free</a></td>
<td>2022-10-26</td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td><a href="vuln-7.85.0.html">7.85.0</a></td>
<td></td>
</tr>
<tr>
<td>128</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2022-35260.html">CVE-2022-35260: .netrc parser out-of-bounds access</a></td>
<td>2022-10-26</td>
<td><a href="vuln-7.84.0.html">7.84.0</a></td>
<td><a href="vuln-7.85.0.html">7.85.0</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>127</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2022-32221.html">CVE-2022-32221: POST following PUT confusion</a></td>
<td>2022-10-26</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.85.0.html">7.85.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>126</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-35252.html">CVE-2022-35252: control code in cookie denial of service</a></td>
<td>2022-08-31</td>
<td><a href="vuln-4.9.html">4.9</a></td>
<td><a href="vuln-7.84.0.html">7.84.0</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>125</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-32208.html">CVE-2022-32208: FTP-KRB bad message verification</a></td>
<td>2022-06-27</td>
<td><a href="vuln-7.16.4.html">7.16.4</a></td>
<td><a href="vuln-7.83.1.html">7.83.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>124</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-32207.html">CVE-2022-32207: Non-preserved file permissions</a></td>
<td>2022-06-27</td>
<td><a href="vuln-7.69.0.html">7.69.0</a></td>
<td><a href="vuln-7.83.1.html">7.83.1</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>123</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-32206.html">CVE-2022-32206: HTTP compression denial of service</a></td>
<td>2022-06-27</td>
<td><a href="vuln-7.57.0.html">7.57.0</a></td>
<td><a href="vuln-7.83.1.html">7.83.1</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>122</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-32205.html">CVE-2022-32205: Set-Cookie denial of service</a></td>
<td>2022-06-27</td>
<td><a href="vuln-7.71.0.html">7.71.0</a></td>
<td><a href="vuln-7.83.1.html">7.83.1</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>121</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-30115.html">CVE-2022-30115: HSTS bypass via trailing dot</a></td>
<td>2022-05-11</td>
<td><a href="vuln-7.82.0.html">7.82.0</a></td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>120</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-27782.html">CVE-2022-27782: TLS and SSH connection too eager reuse</a></td>
<td>2022-05-11</td>
<td><a href="vuln-7.16.1.html">7.16.1</a></td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>119</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2022-27781.html">CVE-2022-27781: CERTINFO never-ending busy-loop</a></td>
<td>2022-05-11</td>
<td><a href="vuln-7.34.0.html">7.34.0</a></td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td></td>
</tr>
<tr>
<td>118</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-27780.html">CVE-2022-27780: percent-encoded path separator in URL host</a></td>
<td>2022-05-11</td>
<td><a href="vuln-7.80.0.html">7.80.0</a></td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>117</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-27779.html">CVE-2022-27779: cookie for trailing dot TLD</a></td>
<td>2022-05-11</td>
<td><a href="vuln-7.82.0.html">7.82.0</a></td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>116</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2022-27778.html">CVE-2022-27778: curl removes wrong file on error</a></td>
<td>2022-05-11</td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td><a href="vuln-7.83.0.html">7.83.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>115</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-27776.html">CVE-2022-27776: Auth/cookie leak on redirect</a></td>
<td>2022-04-27</td>
<td><a href="vuln-4.9.html">4.9</a></td>
<td><a href="vuln-7.82.0.html">7.82.0</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>114</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-27775.html">CVE-2022-27775: Bad local IPv6 connection reuse</a></td>
<td>2022-04-27</td>
<td><a href="vuln-7.65.0.html">7.65.0</a></td>
<td><a href="vuln-7.82.0.html">7.82.0</a></td>
<td>480 USD</td>
</tr>
<tr>
<td>113</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-27774.html">CVE-2022-27774: Credential leak on redirect</a></td>
<td>2022-04-27</td>
<td><a href="vuln-4.9.html">4.9</a></td>
<td><a href="vuln-7.82.0.html">7.82.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>112</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2022-22576.html">CVE-2022-22576: OAUTH2 bearer bypass in connection reuse</a></td>
<td>2022-04-27</td>
<td><a href="vuln-7.33.0.html">7.33.0</a></td>
<td><a href="vuln-7.82.0.html">7.82.0</a></td>
<td>2400 USD</td>
</tr>
<tr>
<td>111</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22947.html">CVE-2021-22947: STARTTLS protocol injection via MITM</a></td>
<td>2021-09-15</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.78.0.html">7.78.0</a></td>
<td>1500 USD</td>
</tr>
<tr>
<td>110</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22946.html">CVE-2021-22946: Protocol downgrade required TLS bypassed</a></td>
<td>2021-09-15</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.78.0.html">7.78.0</a></td>
<td>1000 USD</td>
</tr>
<tr>
<td>109</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2021-22945.html">CVE-2021-22945: UAF and double free in MQTT sending</a></td>
<td>2021-09-15</td>
<td><a href="vuln-7.73.0.html">7.73.0</a></td>
<td><a href="vuln-7.78.0.html">7.78.0</a></td>
<td>1000 USD</td>
</tr>
<tr>
<td>108</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22926.html">CVE-2021-22926: CURLOPT_SSLCERT mix-up with Secure Transport</a></td>
<td>2021-07-21</td>
<td><a href="vuln-7.33.0.html">7.33.0</a></td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td>1000 USD</td>
</tr>
<tr>
<td>107</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: UNINIT"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2021-22925.html">CVE-2021-22925: TELNET stack contents disclosure again</a></td>
<td>2021-07-21</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td>800 USD</td>
</tr>
<tr>
<td>106</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22924.html">CVE-2021-22924: Bad connection reuse due to flawed path name checks</a></td>
<td>2021-07-21</td>
<td><a href="vuln-7.10.4.html">7.10.4</a></td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td>1200 USD</td>
</tr>
<tr>
<td>105</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2021-22923.html">CVE-2021-22923: Metalink download sends credentials</a></td>
<td>2021-07-21</td>
<td><a href="vuln-7.27.0.html">7.27.0</a></td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td>700 USD</td>
</tr>
<tr>
<td>104</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2021-22922.html">CVE-2021-22922: Wrong content via Metalink not discarded</a></td>
<td>2021-07-21</td>
<td><a href="vuln-7.27.0.html">7.27.0</a></td>
<td><a href="vuln-7.77.0.html">7.77.0</a></td>
<td>700 USD</td>
</tr>
<tr>
<td>103</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2021-22901.html">CVE-2021-22901: TLS session caching disaster</a></td>
<td>2021-05-26</td>
<td><a href="vuln-7.75.0.html">7.75.0</a></td>
<td><a href="vuln-7.76.1.html">7.76.1</a></td>
<td>2000 USD</td>
</tr>
<tr>
<td>102</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: UNINIT"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2021-22898.html">CVE-2021-22898: TELNET stack contents disclosure</a></td>
<td>2021-05-26</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.76.1.html">7.76.1</a></td>
<td>1000 USD</td>
</tr>
<tr>
<td>101</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22897.html">CVE-2021-22897: Schannel cipher selection surprise</a></td>
<td>2021-05-26</td>
<td><a href="vuln-7.61.0.html">7.61.0</a></td>
<td><a href="vuln-7.76.1.html">7.76.1</a></td>
<td>800 USD</td>
</tr>
<tr>
<td>100</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22890.html">CVE-2021-22890: TLS 1.3 session ticket proxy host mix-up</a></td>
<td>2021-03-31</td>
<td><a href="vuln-7.63.0.html">7.63.0</a></td>
<td><a href="vuln-7.75.0.html">7.75.0</a></td>
<td></td>
</tr>
<tr>
<td>99</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2021-22876.html">CVE-2021-22876: Automatic referer leaks credentials</a></td>
<td>2021-03-31</td>
<td><a href="vuln-7.1.1.html">7.1.1</a></td>
<td><a href="vuln-7.75.0.html">7.75.0</a></td>
<td>800 USD</td>
</tr>
<tr>
<td>98</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2020-8286.html">CVE-2020-8286: Inferior OCSP verification</a></td>
<td>2020-12-09</td>
<td><a href="vuln-7.41.0.html">7.41.0</a></td>
<td><a href="vuln-7.73.0.html">7.73.0</a></td>
<td>900 USD</td>
</tr>
<tr>
<td>97</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2020-8285.html">CVE-2020-8285: FTP wildcard stack overflow</a></td>
<td>2020-12-09</td>
<td><a href="vuln-7.21.0.html">7.21.0</a></td>
<td><a href="vuln-7.73.0.html">7.73.0</a></td>
<td></td>
</tr>
<tr>
<td>96</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2020-8284.html">CVE-2020-8284: trusting FTP PASV responses</a></td>
<td>2020-12-09</td>
<td><a href="vuln-4.0.html">4.0</a></td>
<td><a href="vuln-7.73.0.html">7.73.0</a></td>
<td>700 USD</td>
</tr>
<tr>
<td>95</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2020-8231.html">CVE-2020-8231: wrong connect-only connection</a></td>
<td>2020-08-19</td>
<td><a href="vuln-7.29.0.html">7.29.0</a></td>
<td><a href="vuln-7.71.1.html">7.71.1</a></td>
<td>500 USD</td>
</tr>
<tr>
<td>94</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2020-8177.html">CVE-2020-8177: curl overwrite local file with -J</a></td>
<td>2020-06-24</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.70.0.html">7.70.0</a></td>
<td>700 USD</td>
</tr>
<tr>
<td>93</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2020-8169.html">CVE-2020-8169: Partial password leak over DNS on HTTP redirect</a></td>
<td>2020-06-24</td>
<td><a href="vuln-7.62.0.html">7.62.0</a></td>
<td><a href="vuln-7.70.0.html">7.70.0</a></td>
<td>400 USD</td>
</tr>
<tr>
<td>92</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2019-5481.html">CVE-2019-5481: FTP-KRB double free</a></td>
<td>2019-09-11</td>
<td><a href="vuln-7.52.0.html">7.52.0</a></td>
<td><a href="vuln-7.65.3.html">7.65.3</a></td>
<td>200 USD</td>
</tr>
<tr>
<td>91</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2019-5482.html">CVE-2019-5482: TFTP small blocksize heap buffer overflow</a></td>
<td>2019-09-11</td>
<td><a href="vuln-7.19.4.html">7.19.4</a></td>
<td><a href="vuln-7.65.3.html">7.65.3</a></td>
<td>250 USD</td>
</tr>
<tr>
<td>90</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2019-5443.html">CVE-2019-5443: Windows OpenSSL engine code injection</a></td>
<td>2019-06-24</td>
<td><a href="vuln-7.44.0.html">7.44.0</a></td>
<td><a href="vuln-7.65.1.html">7.65.1</a></td>
<td>200 USD</td>
</tr>
<tr>
<td>89</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2019-5436.html">CVE-2019-5436: TFTP receive buffer overflow</a></td>
<td>2019-05-22</td>
<td><a href="vuln-7.19.4.html">7.19.4</a></td>
<td><a href="vuln-7.64.1.html">7.64.1</a></td>
<td>200 USD</td>
</tr>
<tr>
<td>88</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2019-5435.html">CVE-2019-5435: Integer overflows in URL parser</a></td>
<td>2019-05-22</td>
<td><a href="vuln-7.62.0.html">7.62.0</a></td>
<td><a href="vuln-7.64.1.html">7.64.1</a></td>
<td>150 USD</td>
</tr>
<tr>
<td>87</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-16890.html">CVE-2018-16890: NTLM type-2 out-of-bounds buffer read</a></td>
<td>2019-02-06</td>
<td><a href="vuln-7.36.0.html">7.36.0</a></td>
<td><a href="vuln-7.63.0.html">7.63.0</a></td>
<td></td>
</tr>
<tr>
<td>86</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2019-3822.html">CVE-2019-3822: NTLMv2 type-3 header stack buffer overflow</a></td>
<td>2019-02-06</td>
<td><a href="vuln-7.36.0.html">7.36.0</a></td>
<td><a href="vuln-7.63.0.html">7.63.0</a></td>
<td></td>
</tr>
<tr>
<td>85</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2019-3823.html">CVE-2019-3823: SMTP end-of-response out-of-bounds read</a></td>
<td>2019-02-06</td>
<td><a href="vuln-7.34.0.html">7.34.0</a></td>
<td><a href="vuln-7.63.0.html">7.63.0</a></td>
<td></td>
</tr>
<tr>
<td>84</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td title="curl tool only">tool</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-16842.html">CVE-2018-16842: warning message out-of-buffer read</a></td>
<td>2018-10-31</td>
<td><a href="vuln-7.14.1.html">7.14.1</a></td>
<td><a href="vuln-7.61.1.html">7.61.1</a></td>
<td>100 USD</td>
</tr>
<tr>
<td>83</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-16840.html">CVE-2018-16840: use after free in handle close</a></td>
<td>2018-10-31</td>
<td><a href="vuln-7.59.0.html">7.59.0</a></td>
<td><a href="vuln-7.61.1.html">7.61.1</a></td>
<td>100 USD</td>
</tr>
<tr>
<td>82</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-16839.html">CVE-2018-16839: SASL password overflow via integer overflow</a></td>
<td>2018-10-31</td>
<td><a href="vuln-7.33.0.html">7.33.0</a></td>
<td><a href="vuln-7.61.1.html">7.61.1</a></td>
<td></td>
</tr>
<tr>
<td>81</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-14618.html">CVE-2018-14618: NTLM password overflow via integer overflow</a></td>
<td>2018-09-05</td>
<td><a href="vuln-7.15.4.html">7.15.4</a></td>
<td><a href="vuln-7.61.0.html">7.61.0</a></td>
<td></td>
</tr>
<tr>
<td>80</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-0500.html">CVE-2018-0500: SMTP send heap buffer overflow</a></td>
<td>2018-07-11</td>
<td><a href="vuln-7.54.1.html">7.54.1</a></td>
<td><a href="vuln-7.60.0.html">7.60.0</a></td>
<td></td>
</tr>
<tr>
<td>79</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-1000300.html">CVE-2018-1000300: FTP shutdown response buffer overflow</a></td>
<td>2018-05-16</td>
<td><a href="vuln-7.54.1.html">7.54.1</a></td>
<td><a href="vuln-7.59.0.html">7.59.0</a></td>
<td></td>
</tr>
<tr>
<td>78</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-1000301.html">CVE-2018-1000301: RTSP bad headers buffer over-read</a></td>
<td>2018-05-16</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.59.0.html">7.59.0</a></td>
<td></td>
</tr>
<tr>
<td>77</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-1000122.html">CVE-2018-1000122: RTSP RTP buffer over-read</a></td>
<td>2018-03-14</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.58.0.html">7.58.0</a></td>
<td></td>
</tr>
<tr>
<td>76</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: NULL_MISTAKE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-1000121.html">CVE-2018-1000121: LDAP NULL pointer dereference</a></td>
<td>2018-03-14</td>
<td><a href="vuln-7.21.0.html">7.21.0</a></td>
<td><a href="vuln-7.58.0.html">7.58.0</a></td>
<td></td>
</tr>
<tr>
<td>75</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-1000120.html">CVE-2018-1000120: FTP path trickery leads to NIL byte out of bounds write</a></td>
<td>2018-03-14</td>
<td><a href="vuln-7.12.3.html">7.12.3</a></td>
<td><a href="vuln-7.58.0.html">7.58.0</a></td>
<td></td>
</tr>
<tr>
<td>74</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2018-1000007.html">CVE-2018-1000007: HTTP authentication leak in redirects</a></td>
<td>2018-01-24</td>
<td><a href="vuln-6.0.html">6.0</a></td>
<td><a href="vuln-7.57.0.html">7.57.0</a></td>
<td></td>
</tr>
<tr>
<td>73</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2018-1000005.html">CVE-2018-1000005: HTTP/2 trailer out-of-bounds read</a></td>
<td>2018-01-24</td>
<td><a href="vuln-7.49.0.html">7.49.0</a></td>
<td><a href="vuln-7.57.0.html">7.57.0</a></td>
<td></td>
</tr>
<tr>
<td>72</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-8818.html">CVE-2017-8818: SSL out of buffer access</a></td>
<td>2017-11-29</td>
<td><a href="vuln-7.56.0.html">7.56.0</a></td>
<td><a href="vuln-7.56.1.html">7.56.1</a></td>
<td></td>
</tr>
<tr>
<td>71</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-8817.html">CVE-2017-8817: FTP wildcard out of bounds read</a></td>
<td>2017-11-29</td>
<td><a href="vuln-7.21.0.html">7.21.0</a></td>
<td><a href="vuln-7.56.1.html">7.56.1</a></td>
<td></td>
</tr>
<tr>
<td>70</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-8816.html">CVE-2017-8816: NTLM buffer overflow via integer overflow</a></td>
<td>2017-11-29</td>
<td><a href="vuln-7.36.0.html">7.36.0</a></td>
<td><a href="vuln-7.56.1.html">7.56.1</a></td>
<td></td>
</tr>
<tr>
<td>69</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-1000257.html">CVE-2017-1000257: IMAP FETCH response out of bounds read</a></td>
<td>2017-10-23</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.56.0.html">7.56.0</a></td>
<td></td>
</tr>
<tr>
<td>68</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-1000254.html">CVE-2017-1000254: FTP PWD response parser out of bounds read</a></td>
<td>2017-10-04</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.55.1.html">7.55.1</a></td>
<td></td>
</tr>
<tr>
<td>67</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-1000101.html">CVE-2017-1000101: URL globbing out of bounds read</a></td>
<td>2017-08-09</td>
<td><a href="vuln-7.34.0.html">7.34.0</a></td>
<td><a href="vuln-7.54.1.html">7.54.1</a></td>
<td></td>
</tr>
<tr>
<td>66</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-1000100.html">CVE-2017-1000100: TFTP sends more than buffer size</a></td>
<td>2017-08-09</td>
<td><a href="vuln-7.15.0.html">7.15.0</a></td>
<td><a href="vuln-7.54.1.html">7.54.1</a></td>
<td></td>
</tr>
<tr>
<td>65</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-1000099.html">CVE-2017-1000099: FILE buffer read out of bounds</a></td>
<td>2017-08-09</td>
<td><a href="vuln-7.54.1.html">7.54.1</a></td>
<td><a href="vuln-7.54.1.html">7.54.1</a></td>
<td></td>
</tr>
<tr>
<td>64</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-9502.html">CVE-2017-9502: URL file scheme drive letter buffer overflow</a></td>
<td>2017-06-14</td>
<td><a href="vuln-7.53.0.html">7.53.0</a></td>
<td><a href="vuln-7.54.0.html">7.54.0</a></td>
<td></td>
</tr>
<tr>
<td>63</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2017-7468.html">CVE-2017-7468: TLS session resumption client cert bypass (again)</a></td>
<td>2017-04-19</td>
<td><a href="vuln-7.52.0.html">7.52.0</a></td>
<td><a href="vuln-7.53.1.html">7.53.1</a></td>
<td></td>
</tr>
<tr>
<td>62</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2017-7407.html">CVE-2017-7407: --write-out out of buffer read</a></td>
<td>2017-04-03</td>
<td><a href="vuln-6.5.html">6.5</a></td>
<td><a href="vuln-7.53.1.html">7.53.1</a></td>
<td></td>
</tr>
<tr>
<td>61</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2017-2629.html">CVE-2017-2629: SSL_VERIFYSTATUS ignored</a></td>
<td>2017-02-22</td>
<td><a href="vuln-7.52.0.html">7.52.0</a></td>
<td><a href="vuln-7.52.1.html">7.52.1</a></td>
<td></td>
</tr>
<tr>
<td>60</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-9594.html">CVE-2016-9594: uninitialized random</a></td>
<td>2016-12-23</td>
<td><a href="vuln-7.52.0.html">7.52.0</a></td>
<td><a href="vuln-7.52.0.html">7.52.0</a></td>
<td></td>
</tr>
<tr>
<td>59</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-9586.html">CVE-2016-9586: printf floating point buffer overflow</a></td>
<td>2016-12-21</td>
<td><a href="vuln-5.4.html">5.4</a></td>
<td><a href="vuln-7.51.0.html">7.51.0</a></td>
<td></td>
</tr>
<tr>
<td>58</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-9952.html">CVE-2016-9952: Win CE Schannel cert wildcard matches too much</a></td>
<td>2016-12-21</td>
<td><a href="vuln-7.27.0.html">7.27.0</a></td>
<td><a href="vuln-7.51.0.html">7.51.0</a></td>
<td></td>
</tr>
<tr>
<td>57</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-9953.html">CVE-2016-9953: Win CE Schannel cert name out of buffer read</a></td>
<td>2016-12-21</td>
<td><a href="vuln-7.27.0.html">7.27.0</a></td>
<td><a href="vuln-7.51.0.html">7.51.0</a></td>
<td></td>
</tr>
<tr>
<td>56</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-8615.html">CVE-2016-8615: cookie injection for other servers</a></td>
<td>2016-11-02</td>
<td><a href="vuln-4.9.html">4.9</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>55</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-8616.html">CVE-2016-8616: case insensitive password comparison</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>54</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8617.html">CVE-2016-8617: OOB write via unchecked multiplication</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.8.1.html">7.8.1</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>53</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8618.html">CVE-2016-8618: double free in curl_maprintf</a></td>
<td>2016-11-02</td>
<td><a href="vuln-5.4.html">5.4</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>52</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: DOUBLE_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8619.html">CVE-2016-8619: double free in krb5 code</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.3.html">7.3</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>51</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="curl tool only">tool</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8620.html">CVE-2016-8620: glob parser write/read out of bounds</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.34.0.html">7.34.0</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>50</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8621.html">CVE-2016-8621: curl_getdate read out of bounds</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.12.2.html">7.12.2</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>49</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8622.html">CVE-2016-8622: URL unescape heap overflow via integer truncation</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.24.0.html">7.24.0</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>48</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-8623.html">CVE-2016-8623: Use after free via shared cookies</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.10.7.html">7.10.7</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>47</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-8624.html">CVE-2016-8624: invalid URL parsing with '#'</a></td>
<td>2016-11-02</td>
<td><a href="vuln-6.0.html">6.0</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>46</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-8625.html">CVE-2016-8625: IDNA 2003 makes curl use wrong host</a></td>
<td>2016-11-02</td>
<td><a href="vuln-7.12.0.html">7.12.0</a></td>
<td><a href="vuln-7.50.3.html">7.50.3</a></td>
<td></td>
</tr>
<tr>
<td>45</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-7167.html">CVE-2016-7167: curl escape and unescape integer overflows</a></td>
<td>2016-09-14</td>
<td><a href="vuln-7.11.1.html">7.11.1</a></td>
<td><a href="vuln-7.50.2.html">7.50.2</a></td>
<td></td>
</tr>
<tr>
<td>44</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-7141.html">CVE-2016-7141: Incorrect reuse of client certificates</a></td>
<td>2016-09-07</td>
<td><a href="vuln-7.19.6.html">7.19.6</a></td>
<td><a href="vuln-7.50.1.html">7.50.1</a></td>
<td></td>
</tr>
<tr>
<td>43</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-5419.html">CVE-2016-5419: TLS session resumption client cert bypass</a></td>
<td>2016-08-03</td>
<td><a href="vuln-5.0.html">5.0</a></td>
<td><a href="vuln-7.50.0.html">7.50.0</a></td>
<td></td>
</tr>
<tr>
<td>42</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-5420.html">CVE-2016-5420: Reusing connections with wrong client cert</a></td>
<td>2016-08-03</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.50.0.html">7.50.0</a></td>
<td></td>
</tr>
<tr>
<td>41</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: USE_AFTER_FREE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2016-5421.html">CVE-2016-5421: use of connection struct after free</a></td>
<td>2016-08-03</td>
<td><a href="vuln-7.32.0.html">7.32.0</a></td>
<td><a href="vuln-7.50.0.html">7.50.0</a></td>
<td></td>
</tr>
<tr>
<td>40</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-4802.html">CVE-2016-4802: Windows DLL hijacking</a></td>
<td>2016-05-30</td>
<td><a href="vuln-7.11.1.html">7.11.1</a></td>
<td><a href="vuln-7.49.0.html">7.49.0</a></td>
<td></td>
</tr>
<tr>
<td>39</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-3739.html">CVE-2016-3739: TLS certificate check bypass with mbedTLS/PolarSSL</a></td>
<td>2016-05-18</td>
<td><a href="vuln-7.21.0.html">7.21.0</a></td>
<td><a href="vuln-7.48.0.html">7.48.0</a></td>
<td></td>
</tr>
<tr>
<td>38</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2016-0754.html">CVE-2016-0754: remote filename path traversal in curl tool for Windows</a></td>
<td>2016-01-27</td>
<td><a href="vuln-4.0.html">4.0</a></td>
<td><a href="vuln-7.46.0.html">7.46.0</a></td>
<td></td>
</tr>
<tr>
<td>37</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2016-0755.html">CVE-2016-0755: NTLM credentials not-checked for proxy connection reuse</a></td>
<td>2016-01-27</td>
<td><a href="vuln-7.10.7.html">7.10.7</a></td>
<td><a href="vuln-7.46.0.html">7.46.0</a></td>
<td></td>
</tr>
<tr>
<td>36</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2015-3237.html">CVE-2015-3237: SMB send off unrelated memory contents</a></td>
<td>2015-06-17</td>
<td><a href="vuln-7.40.0.html">7.40.0</a></td>
<td><a href="vuln-7.42.1.html">7.42.1</a></td>
<td></td>
</tr>
<tr>
<td>35</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2015-3236.html">CVE-2015-3236: lingering HTTP credentials in connection reuse</a></td>
<td>2015-06-17</td>
<td><a href="vuln-7.40.0.html">7.40.0</a></td>
<td><a href="vuln-7.42.1.html">7.42.1</a></td>
<td></td>
</tr>
<tr>
<td>34</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2015-3153.html">CVE-2015-3153: sensitive HTTP server headers also sent to proxies</a></td>
<td>2015-04-29</td>
<td><a href="vuln-4.0.html">4.0</a></td>
<td><a href="vuln-7.42.0.html">7.42.0</a></td>
<td></td>
</tr>
<tr>
<td>33</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2015-3144.html">CVE-2015-3144: hostname out of boundary memory access</a></td>
<td>2015-04-22</td>
<td><a href="vuln-7.37.0.html">7.37.0</a></td>
<td><a href="vuln-7.41.0.html">7.41.0</a></td>
<td></td>
</tr>
<tr>
<td>32</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2015-3145.html">CVE-2015-3145: cookie parser out of boundary memory access</a></td>
<td>2015-04-22</td>
<td><a href="vuln-7.31.0.html">7.31.0</a></td>
<td><a href="vuln-7.41.0.html">7.41.0</a></td>
<td></td>
</tr>
<tr>
<td>31</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2015-3148.html">CVE-2015-3148: Negotiate not treated as connection-oriented</a></td>
<td>2015-04-22</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.41.0.html">7.41.0</a></td>
<td></td>
</tr>
<tr>
<td>30</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2015-3143.html">CVE-2015-3143: Reusing authenticated connection when unauthenticated</a></td>
<td>2015-04-22</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.41.0.html">7.41.0</a></td>
<td></td>
</tr>
<tr>
<td>29</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-8151.html">CVE-2014-8151: Secure Transport certificate check bypass</a></td>
<td>2015-01-08</td>
<td><a href="vuln-7.31.0.html">7.31.0</a></td>
<td><a href="vuln-7.39.0.html">7.39.0</a></td>
<td></td>
</tr>
<tr>
<td>28</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-8150.html">CVE-2014-8150: URL request injection</a></td>
<td>2015-01-08</td>
<td><a href="vuln-6.0.html">6.0</a></td>
<td><a href="vuln-7.39.0.html">7.39.0</a></td>
<td></td>
</tr>
<tr>
<td>27</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2014-3707.html">CVE-2014-3707: duphandle read out of bounds</a></td>
<td>2014-11-05</td>
<td><a href="vuln-7.17.1.html">7.17.1</a></td>
<td><a href="vuln-7.38.0.html">7.38.0</a></td>
<td></td>
</tr>
<tr>
<td>26</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-3620.html">CVE-2014-3620: cookie leak for TLDs</a></td>
<td>2014-09-10</td>
<td><a href="vuln-7.31.0.html">7.31.0</a></td>
<td><a href="vuln-7.37.1.html">7.37.1</a></td>
<td></td>
</tr>
<tr>
<td>25</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-3613.html">CVE-2014-3613: cookie leak with IP address as domain</a></td>
<td>2014-09-10</td>
<td><a href="vuln-4.0.html">4.0</a></td>
<td><a href="vuln-7.37.1.html">7.37.1</a></td>
<td></td>
</tr>
<tr>
<td>24</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-2522.html">CVE-2014-2522: not verifying certs for TLS to IP address / Schannel</a></td>
<td>2014-03-26</td>
<td><a href="vuln-7.27.0.html">7.27.0</a></td>
<td><a href="vuln-7.35.0.html">7.35.0</a></td>
<td></td>
</tr>
<tr>
<td>23</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-1263.html">CVE-2014-1263: not verifying certs for TLS to IP address / Secure Transport</a></td>
<td>2014-03-26</td>
<td><a href="vuln-7.27.0.html">7.27.0</a></td>
<td><a href="vuln-7.35.0.html">7.35.0</a></td>
<td></td>
</tr>
<tr>
<td>22</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-0139.html">CVE-2014-0139: IP address wildcard certificate validation</a></td>
<td>2014-03-26</td>
<td><a href="vuln-7.10.3.html">7.10.3</a></td>
<td><a href="vuln-7.35.0.html">7.35.0</a></td>
<td></td>
</tr>
<tr>
<td>21</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-0138.html">CVE-2014-0138: wrong reuse of connections</a></td>
<td>2014-03-26</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.35.0.html">7.35.0</a></td>
<td></td>
</tr>
<tr>
<td>20</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2014-0015.html">CVE-2014-0015: reuse of wrong HTTP NTLM connection</a></td>
<td>2014-01-29</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.34.0.html">7.34.0</a></td>
<td></td>
</tr>
<tr>
<td>19</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2013-6422.html">CVE-2013-6422: cert name check ignore with GnuTLS</a></td>
<td>2013-12-17</td>
<td><a href="vuln-7.21.4.html">7.21.4</a></td>
<td><a href="vuln-7.33.0.html">7.33.0</a></td>
<td></td>
</tr>
<tr>
<td>18</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2013-4545.html">CVE-2013-4545: cert name check ignore OpenSSL</a></td>
<td>2013-11-15</td>
<td><a href="vuln-7.18.0.html">7.18.0</a></td>
<td><a href="vuln-7.32.0.html">7.32.0</a></td>
<td></td>
</tr>
<tr>
<td>17</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td title="libcurl only">lib</td>
<td title="C mistake: OVERREAD"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2013-2174.html">CVE-2013-2174: URL decode buffer boundary flaw</a></td>
<td>2013-06-22</td>
<td><a href="vuln-7.7.html">7.7</a></td>
<td><a href="vuln-7.30.0.html">7.30.0</a></td>
<td></td>
</tr>
<tr>
<td>16</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2013-1944.html">CVE-2013-1944: cookie domain tailmatch</a></td>
<td>2013-04-12</td>
<td><a href="vuln-4.7.html">4.7</a></td>
<td><a href="vuln-7.29.0.html">7.29.0</a></td>
<td></td>
</tr>
<tr>
<td>15</td>
<td title="Severity Critical"><div style="color: black; border-radius: 8px; border: 2px black solid; text-align: center;">C</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2013-0249.html">CVE-2013-0249: SASL buffer overflow</a></td>
<td>2013-02-06</td>
<td><a href="vuln-7.26.0.html">7.26.0</a></td>
<td><a href="vuln-7.28.1.html">7.28.1</a></td>
<td></td>
</tr>
<tr>
<td>14</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2011-3389.html">CVE-2011-3389: SSL CBC IV vulnerability</a></td>
<td>2012-01-24</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.23.1.html">7.23.1</a></td>
<td></td>
</tr>
<tr>
<td>13</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2012-0036.html">CVE-2012-0036: URL sanitization vulnerability</a></td>
<td>2012-01-24</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.23.1.html">7.23.1</a></td>
<td></td>
</tr>
<tr>
<td>12</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2011-2192.html">CVE-2011-2192: inappropriate GSSAPI delegation</a></td>
<td>2011-06-23</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.21.6.html">7.21.6</a></td>
<td></td>
</tr>
<tr>
<td>11</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td title="curl tool only">tool</td>
<td></td>
<td><a href="CVE-2010-3842.html">CVE-2010-3842: local file overwrite</a></td>
<td>2010-10-13</td>
<td><a href="vuln-7.20.0.html">7.20.0</a></td>
<td><a href="vuln-7.21.1.html">7.21.1</a></td>
<td></td>
</tr>
<tr>
<td>10</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td title="libcurl only">lib</td>
<td></td>
<td><a href="CVE-2010-0734.html">CVE-2010-0734: data callback excessive length</a></td>
<td>2010-02-09</td>
<td><a href="vuln-7.10.5.html">7.10.5</a></td>
<td><a href="vuln-7.19.7.html">7.19.7</a></td>
<td></td>
</tr>
<tr>
<td>9</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: NULL_MISTAKE"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2009-2417.html">CVE-2009-2417: embedded zero in cert name</a></td>
<td>2009-08-12</td>
<td><a href="vuln-7.4.html">7.4</a></td>
<td><a href="vuln-7.19.5.html">7.19.5</a></td>
<td></td>
</tr>
<tr>
<td>8</td>
<td title="Severity Medium"><div style="color: blue; border-radius: 8px; border: 2px blue solid; text-align: center;">M</div></td>
<td></td>
<td></td>
<td><a href="CVE-2009-0037.html">CVE-2009-0037: Arbitrary File Access</a></td>
<td>2009-03-03</td>
<td><a href="vuln-5.11.html">5.11</a></td>
<td><a href="vuln-7.19.3.html">7.19.3</a></td>
<td></td>
</tr>
<tr>
<td>7</td>
<td title="Severity Low"><div style="color: green; border-radius: 8px; border: 2px green solid; text-align: center;">L</div></td>
<td></td>
<td></td>
<td><a href="CVE-2007-3564.html">CVE-2007-3564: GnuTLS insufficient cert verification</a></td>
<td>2007-07-10</td>
<td><a href="vuln-7.14.0.html">7.14.0</a></td>
<td><a href="vuln-7.16.3.html">7.16.3</a></td>
<td></td>
</tr>
<tr>
<td>6</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2006-1061.html">CVE-2006-1061: TFTP Packet Buffer Overflow</a></td>
<td>2006-03-20</td>
<td><a href="vuln-7.15.0.html">7.15.0</a></td>
<td><a href="vuln-7.15.2.html">7.15.2</a></td>
<td></td>
</tr>
<tr>
<td>5</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2005-4077.html">CVE-2005-4077: URL Buffer Overflow</a></td>
<td>2005-12-07</td>
<td><a href="vuln-7.11.2.html">7.11.2</a></td>
<td><a href="vuln-7.15.0.html">7.15.0</a></td>
<td></td>
</tr>
<tr>
<td>4</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2005-3185.html">CVE-2005-3185: NTLM Buffer Overflow</a></td>
<td>2005-10-13</td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td><a href="vuln-7.14.1.html">7.14.1</a></td>
<td></td>
</tr>
<tr>
<td>3</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2005-0490.html">CVE-2005-0490: Authentication Buffer Overflows</a></td>
<td>2005-02-21</td>
<td><a href="vuln-7.3.html">7.3</a></td>
<td><a href="vuln-7.13.0.html">7.13.0</a></td>
<td></td>
</tr>
<tr>
<td>2</td>
<td title="Severity High"><div style="color: red; border-radius: 8px; border: 2px red solid; text-align: center;">H</div></td>
<td></td>
<td></td>
<td><a href="CVE-2003-1605.html">CVE-2003-1605: Proxy Authentication Header Information Leakage</a></td>
<td>2003-08-03</td>
<td><a href="vuln-4.5.html">4.5</a></td>
<td><a href="vuln-7.10.6.html">7.10.6</a></td>
<td></td>
</tr>
<tr>
<td>1</td>
<td title="Severity Critical"><div style="color: black; border-radius: 8px; border: 2px black solid; text-align: center;">C</div></td>
<td></td>
<td title="C mistake: OVERFLOW"><div style="color: ; border-radius: 12px; border: 2px black dotted; text-align: center;">C</div></td>
<td><a href="CVE-2000-0973.html">CVE-2000-0973: FTP Server Response Buffer Overflow</a></td>
<td>2000-10-13</td>
<td><a href="vuln-6.0.html">6.0</a></td>
<td><a href="vuln-7.4.html">7.4</a></td>
<td></td>
</tr>
</table>
<h2> Published vulnerabilities for wcurl </h2>
<p>
  <a href="CVE-2025-11563.html">CVE-2025-11563: path traversal with percent-encoded slashes</a>
<h2> C mistakes </h2>
<p>
 Flaws listed as "C mistakes" are vulnerabilities that we deem
 are <i>likely</i> to not have happened should we have used a memory-safe
 language rather than C. The C mistakes are divided into the following areas:
 OVERFLOW, OVERREAD, DOUBLE_FREE, USE_AFTER_FREE, NULL_MISTAKE, UNINIT and
 BAD_FREE.
<h2> Retracted security vulnerabilities </h2>
<p>
  Issues no longer considered curl security problems:
<ul>
<li> <a href="CVE-2019-15601.html">CVE-2019-15601</a> - SMB access smuggling via FILE URL on Windows
<li> <a href="CVE-2023-32001.html">CVE-2023-32001</a> - fopen race condition
</ul>
<h2> Bogus security vulnerabilities </h2>
<p>
  Issues filed by others that are plain lies:
<ul>
<li> <a href="CVE-2020-19909.html">CVE-2020-19909</a>
<li> <a href="CVE-2023-52071.html">CVE-2023-52071</a>
</ul>
<h2> curl vulnerability data </h2>
<p>
 <a href="vuln.csv">vuln.csv</a> and <a href="vuln.json">vuln.json</a> provide
 info about all vulnerabilities in machine friendly formats.
<p>
 Each vulnerability is also provided as a single JSON that you can access at
 "https://curl.se/docs/$CVE.json" - replace $CVE with the actual curl CVE Id.
<p>
 The JSON output follows the <a href="https://ossf.github.io/osv-schema/">Open
 Source Vulnerability format</a>
</div>
</div>
</body> </html>
