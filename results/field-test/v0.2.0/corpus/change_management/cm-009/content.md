<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!-- force IE browsers in compatibility mode to use their most aggressive rendering engine -->

    <meta charset="utf-8">
    <title>GitHub Status - Incident History</title>
    <meta name="description" content="GitHub&#39;s Incident and Scheduled Maintenance History">

    <!-- Mobile viewport optimization -->
    <meta name="HandheldFriendly" content="True">
    <meta name="MobileOptimized" content="320">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0">

    <!-- Time this page was rendered - http://purl.org/dc/terms/issued -->
    <meta name="issued" content="1787883396">

    <!-- Mobile IE allows us to activate ClearType technology for smoothing fonts for easy reading -->
    <meta http-equiv="cleartype" content="on">

      <!-- Atlassian Sans & Mono Fonts -->
<link
  rel="preconnect"
  href="https://ds-cdn.prod-east.frontend.public.atl-paas.net" />
<link
  rel="preload"
  href="https://ds-cdn.prod-east.frontend.public.atl-paas.net/assets/fonts/atlassian-sans/v3/AtlassianSans-latin.woff2"
  as="font" type="font/woff2" crossorigin />
<link
  rel="preload"
  href="https://ds-cdn.prod-east.frontend.public.atl-paas.net/assets/font-rules/v5/atlassian-fonts.css"
  as="style" crossorigin />

    <style>
  /* Dynamic Font Stack based on Feature Flag */
    /* Using Atlassian Sans & Mono */
    :root {
      --font-stack-a: "Atlassian Sans", "Helvetica Neue", Helvetica, Arial, Sans-Serif;
      --font-stack-b: "Atlassian Mono", "SFMono-Medium", "SF Mono", "Segoe UI Mono", "Roboto Mono", "Ubuntu Mono", Menlo, Consolas, Courier, monospace;
    }
</style>


      <link rel="shortcut icon" type="image/x-icon" href="//dka575ofm4ao0.cloudfront.net/pages-favicon_logos/original/36420/akacZEQQfOBdc7ftyxJt" />

    <link rel="shortcut icon" href='//dka575ofm4ao0.cloudfront.net/pages-favicon_logos/original/36420/akacZEQQfOBdc7ftyxJt'>

    <link rel="alternate" type="application/atom+xml" href="https://www.githubstatus.com/history.atom" title="GitHub Status History - Atom Feed">
    <link rel="alternate" type="application/rss+xml" href="https://www.githubstatus.com/history.rss" title="GitHub Status History - RSS Feed">

      <!-- Canonical Link to ensure that only the custom domain is indexed when present -->
      <link rel="canonical" href="https://www.githubstatus.com/history">

    <meta name="_globalsign-domain-verification" content="y_VzfckMy4iePo5oDJNivyYIjh8LffYa4jzUndm_bZ"/>


    <link rel="alternate" type="application/atom+xml" title="ATOM" href="https://www.githubstatus.com/history.atom" />

    <!-- Le styles -->
    <link rel="stylesheet" media="screen" href="https://dka575ofm4ao0.cloudfront.net/packs/0.042e2683dd61b94e3981.css" /><link rel="stylesheet" media="screen" href="https://dka575ofm4ao0.cloudfront.net/packs/191.042e2683dd61b94e3981.css" /><link rel="stylesheet" media="screen" href="https://dka575ofm4ao0.cloudfront.net/packs/155.042e2683dd61b94e3981.css" />
    <link rel="stylesheet" media="all" href="https://dka575ofm4ao0.cloudfront.net/assets/status/status_manifest-3975cac43f498cd81d991d1abc986307c014f9c6ec29a9abfeb3b0882674850a.css" />

    <script src="https://dka575ofm4ao0.cloudfront.net/assets/jquery-3.5.1.min-729e416557a365062a8a20f0562f18aa171da57298005d392312670c706c68de.js"></script>

    <script>
      window.pageColorData = {"blue":"#0366d6","border":"#e1e4e8","body_background":"#ffffff","font":"#24292e","graph":"#0366d6","green":"#28a745","light_font":"#6a737d","link":"#0366d6","orange":"#e36209","red":"#dc3545","yellow":"#dbab09","no_data":"#b3bac5"};
    </script>
    <style>
  /* BODY BACKGROUND */ /* BODY BACKGROUND */ /* BODY BACKGROUND */ /* BODY BACKGROUND */ /* BODY BACKGROUND */
  body,
  .layout-content.status.status-api .section .example-container .example-opener .color-secondary,
  .grouped-items-selector,
  .layout-content.status.status-full-history .history-nav a.current,
  div[id^="subscribe-modal"] .modal-footer,
  div[id^="subscribe-modal"],
  div[id^="updates-dropdown"] .updates-dropdown-section,
  #uptime-tooltip .tooltip-box {
    background-color:#ffffff;
  }

  #uptime-tooltip .pointer-container .pointer-smaller {
    border-bottom-color:#ffffff;
  }




  /* PRIMARY FONT COLOR */ /* PRIMARY FONT COLOR */ /* PRIMARY FONT COLOR */ /* PRIMARY FONT COLOR */
  body.status,
  .color-primary,
  .color-primary:hover,
  .layout-content.status-index .status-day .update-title.impact-none a,
  .layout-content.status-index .status-day .update-title.impact-none a:hover,
  .layout-content.status-index .timeframes-container .timeframe.active,
  .layout-content.status-full-history .month .incident-container .impact-none,
  .layout-content.status.status-index .incidents-list .incident-title.impact-none a,
  .incident-history .impact-none,
  .layout-content.status .grouped-items-selector.inline .grouped-item.active,
  .layout-content.status.status-full-history .history-nav a.current,
  .layout-content.status.status-full-history .history-nav a:not(.current):hover,
  div[id^="subscribe-modal"] .modal-header .close,
  .grouped-item-label,
  #uptime-tooltip .tooltip-box .tooltip-content .related-events .related-event a.related-event-link {
    color:#24292e;
  }

  .layout-content.status.status-index .components-statuses .component-container .name {
    color:#24292e;
    color:rgba(36,41,46,.8);
  }




  /* SECONDARY FONT COLOR */ /* SECONDARY FONT COLOR */ /* SECONDARY FONT COLOR */ /* SECONDARY FONT COLOR */
  small,
  .layout-content.status .table-row .date,
  .color-secondary,
  .layout-content.status .grouped-items-selector.inline .grouped-item,
  .layout-content.status.status-full-history .history-footer .pagination a.disabled,
  .layout-content.status.status-full-history .history-nav a,
  #uptime-tooltip .tooltip-box .tooltip-content .related-events #related-event-header {
    color:#6a737d;
  }




  /* BORDER COLOR */  /* BORDER COLOR */  /* BORDER COLOR */  /* BORDER COLOR */  /* BORDER COLOR */  /* BORDER COLOR */
  body.status .layout-content.status .border-color,
  hr,
  .tooltip-base,
  .markdown-display table,
  div[id^="subscribe-modal"],
  #uptime-tooltip .tooltip-box {
    border-color:#e1e4e8;
  }

  div[id^="subscribe-modal"] .modal-footer,
  .markdown-display table td {
    border-top-color:#e1e4e8;
  }

  .markdown-display table td + td, .markdown-display table th + th {
    border-left-color:#e1e4e8;
  }

  div[id^="subscribe-modal"] .modal-header,
  #uptime-tooltip .pointer-container .pointer-larger {
    border-bottom-color:#e1e4e8;
  }

  #uptime-tooltip .tooltip-box .outage-field {
    /*
      Generate the background-color for the outage-field from the css_body_background_color and css_border_color.

      For the default background (#ffffff) and default css_border_color (#e0e0e0), use the luminosity of the default background with a magic number to arrive at
      the original outage-field background color (#f4f5f7). I used the formula Target Color = Color * alpha + Background * (1 - alpha) to find the magic number of ~0.08.

      For darker css_body_background_color, luminosity values are lower so alpha trends toward becoming transparent (thus outage-field background becomes same as css_body_background_color).
    */
    background-color: rgba(225,228,232,0.31);

    /*
      outage-field border-color alpha is inverse to the luminosity of css_body_background_color.
      That is to say, with a default white background this border is transparent, but on a black background, it's opaque css_border_color.
    */
    border-color: rgba(225,228,232,0.0);
  }




  /* CSS REDS */ /* CSS REDS */ /* CSS REDS */ /* CSS REDS */ /* CSS REDS */ /* CSS REDS */ /* CSS REDS */
  .layout-content.status.status-index .status-day .update-title.impact-critical a,
  .layout-content.status.status-index .status-day .update-title.impact-critical a:hover,
  .layout-content.status.status-index .page-status.status-critical,
  .layout-content.status.status-index .unresolved-incident.impact-critical .incident-title,
  .flat-button.background-red {
    background-color:#dc3545;
  }

  .layout-content.status-index .components-statuses .component-container.status-red:after,
  .layout-content.status-full-history .month .incident-container .impact-critical,
  .layout-content.status-incident .incident-name.impact-critical,
  .layout-content.status.status-index .incidents-list .incident-title.impact-critical a,
  .status-red .icon-indicator,
  .incident-history .impact-critical,
  .components-container .component-inner-container.status-red .component-status,
  .components-container .component-inner-container.status-red .icon-indicator {
    color:#dc3545;
  }

  .layout-content.status.status-index .unresolved-incident.impact-critical .updates {
    border-color:#dc3545;
  }




  /* CSS ORANGES */ /* CSS ORANGES */ /* CSS ORANGES */ /* CSS ORANGES */ /* CSS ORANGES */ /* CSS ORANGES */
  .layout-content.status.status-index .status-day .update-title.impact-major a,
  .layout-content.status.status-index .status-day .update-title.impact-major a:hover,
  .layout-content.status.status-index .page-status.status-major,
  .layout-content.status.status-index .unresolved-incident.impact-major .incident-title {
    background-color:#e36209;
  }

  .layout-content.status-index .components-statuses .component-container.status-orange:after,
  .layout-content.status-full-history .month .incident-container .impact-major,
  .layout-content.status-incident .incident-name.impact-major,
  .layout-content.status.status-index .incidents-list .incident-title.impact-major a,
  .status-orange .icon-indicator,
  .incident-history .impact-major,
  .components-container .component-inner-container.status-orange .component-status,
  .components-container .component-inner-container.status-orange .icon-indicator {
    color:#e36209;
  }

  .layout-content.status.status-index .unresolved-incident.impact-major .updates {
    border-color:#e36209;
  }




  /* CSS YELLOWS */ /* CSS YELLOWS */ /* CSS YELLOWS */ /* CSS YELLOWS */ /* CSS YELLOWS */ /* CSS YELLOWS */
  .layout-content.status.status-index .status-day .update-title.impact-minor a,
  .layout-content.status.status-index .status-day .update-title.impact-minor a:hover,
  .layout-content.status.status-index .page-status.status-minor,
  .layout-content.status.status-index .unresolved-incident.impact-minor .incident-title,
  .layout-content.status.status-index .scheduled-incidents-container .tab {
    background-color:#dbab09;
  }

  .layout-content.status-index .components-statuses .component-container.status-yellow:after,
  .layout-content.status-full-history .month .incident-container .impact-minor,
  .layout-content.status-incident .incident-name.impact-minor,
  .layout-content.status.status-index .incidents-list .incident-title.impact-minor a,
  .status-yellow .icon-indicator,
  .incident-history .impact-minor,
  .components-container .component-inner-container.status-yellow .component-status,
  .components-container .component-inner-container.status-yellow .icon-indicator,
  .layout-content.status.manage-subscriptions .confirmation-infobox .fa {
    color:#dbab09;
  }

  .layout-content.status.status-index .unresolved-incident.impact-minor .updates,
  .layout-content.status.status-index .scheduled-incidents-container {
    border-color:#dbab09;
  }




  /* CSS BLUES */ /* CSS BLUES */ /* CSS BLUES */ /* CSS BLUES */ /* CSS BLUES */ /* CSS BLUES */
  .layout-content.status.status-index .status-day .update-title.impact-maintenance a,
  .layout-content.status.status-index .status-day .update-title.impact-maintenance a:hover,
  .layout-content.status.status-index .page-status.status-maintenance,
  .layout-content.status.status-index .unresolved-incident.impact-maintenance .incident-title,
  .layout-content.status.status-index .scheduled-incidents-container .tab {
    background-color:#0366d6;
  }

  .layout-content.status-index .components-statuses .component-container.status-blue:after,
  .layout-content.status-full-history .month .incident-container .impact-maintenance,
  .layout-content.status-incident .incident-name.impact-maintenance,
  .layout-content.status.status-index .incidents-list .incident-title.impact-maintenance a,
  .status-blue .icon-indicator,
  .incident-history .impact-maintenance,
  .components-container .component-inner-container.status-blue .component-status,
  .components-container .component-inner-container.status-blue .icon-indicator {
    color:#0366d6;
  }

  .layout-content.status.status-index .unresolved-incident.impact-maintenance .updates,
  .layout-content.status.status-index .scheduled-incidents-container {
    border-color:#0366d6;
  }




  /* CSS GREENS */ /* CSS GREENS */ /* CSS GREENS */ /* CSS GREENS */ /* CSS GREENS */ /* CSS GREENS */ /* CSS GREENS */
  .layout-content.status.status-index .page-status.status-none {
    background-color:#28a745;
  }
  .layout-content.status-index .components-statuses .component-container.status-green:after,
  .status-green .icon-indicator,
  .components-container .component-inner-container.status-green .component-status,
  .components-container .component-inner-container.status-green .icon-indicator {
    color:#28a745;
  }




  /* CSS LINK COLOR */  /* CSS LINK COLOR */  /* CSS LINK COLOR */  /* CSS LINK COLOR */  /* CSS LINK COLOR */  /* CSS LINK COLOR */
  a,
  a:hover,
  .layout-content.status-index .page-footer span a:hover,
  .layout-content.status-index .timeframes-container .timeframe:not(.active):hover,
  .layout-content.status-incident .subheader a:hover {
    color:#0366d6;
  }

  .flat-button,
  .masthead .updates-dropdown-container .show-updates-dropdown,
  .layout-content.status-full-history .show-filter.open  {
    background-color:#0366d6;
  }




  /* CUSTOM COLOR OVERRIDES FOR UPTIME SHOWCASE */
  .components-section .components-uptime-link {
    color: #6a737d;
  }

  .layout-content.status .shared-partial.uptime-90-days-wrapper .legend .legend-item {
    color: #6a737d;
    opacity: 1;
  }
  .layout-content.status .shared-partial.uptime-90-days-wrapper .legend .legend-item.light {
    color: #6a737d;
    opacity: 1;
  }
  .layout-content.status .shared-partial.uptime-90-days-wrapper .legend .spacer {
    background: #6a737d;
    opacity: 1;
  }
</style>


    <!-- custom css -->
        <link rel="stylesheet" type="text/css" href="//dka575ofm4ao0.cloudfront.net/page_display_customizations-custom_css_externals/36313/external20260821-27171-l4y3j7.css">

      <!-- polyfills -->
        <script crossorigin="anonymous" src="https://cdnjs.cloudflare.com/polyfill/v3/polyfill.js"></script>

    <!-- Le HTML5 shim -->
    <!--[if lt IE 9]>
      <script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- injection for static -->


    
  </head>


  <body class="status history status-none a11y-focus-indicators">

    
<div class="layout-content status status-full-history starter">

    <div class="custom-header-container">
    <script>
  var meta = document.createElement('meta');
  meta.setAttribute('name', 'ha-url');
  meta.setAttribute('content', 'https://collector.githubapp.com/statuspage-views/collect');
  document.head.appendChild(meta);
</script>
<script async onload="initAnalytics()" src="https://analytics.githubassets.com/hydro-client.min.js"></script>
<script>
  function initAnalytics() {
    if (!window._ha) {
      return
    }

    // Send general pageview
    window._ha.sendPageView()

    // If on homepage, send index page view only if not a page refresh
    if (window.location.pathname === '/' &&
      document.referrer !== (document.location.origin + document.location.pathname)) {
      let indexHa = Object.create(window._ha);
      indexHa.options = { ...window._ha.options }
      indexHa.options.collectorUrl = 'https://collector.githubapp.com/statuspage/collect';
      indexHa.sendPageView();
    }
  }
</script>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    // Select the Twitter button
    var twitterBtn = document.getElementById("updates-dropdown-twitter-btn");

    if (twitterBtn) {
      twitterBtn.innerHTML = `
  <span class="icon-container x" style="height: 100%; display: flex; align-items: center; justify-content: center;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20" role="img">
      <title>Subscribe via X</title>
      <path fill="currentColor" d="M14.28 10.38L23.2 0h-2.1L13.8 9.02L7.14 0H0l10.13 14.7L0 25.5h2.1l7.64-9.38l6.9 9.38H23.2L12.72 10.38zM3.06 1.62h2.76L20.94 23.9h-2.76L3.06 1.62z"/>
    </svg>
  </span>
`;
    }
  });
</script>

<div
  class="header d-md-flex flex-md-justify-between flex-md-items-center px-4 py-3 text-center text-md-left bg-white box-shadow-large">
  <a href="/" aria-label="GitHub Octicon logo" style="height: 32px;">
    <svg viewBox="0 0 98 96" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32">
      <title>GitHub Octicon logo</title>
      <g clip-path="url(#clip0_730_27126)">
        <path
          d="M41.4395 69.3848C28.8066 67.8535 19.9062 58.7617 19.9062 46.9902C19.9062 42.2051 21.6289 37.0371 24.5 33.5918C23.2559 30.4336 23.4473 23.7344 24.8828 20.959C28.7109 20.4805 33.8789 22.4902 36.9414 25.2656C40.5781 24.1172 44.4062 23.543 49.0957 23.543C53.7852 23.543 57.6133 24.1172 61.0586 25.1699C64.0254 22.4902 69.2891 20.4805 73.1172 20.959C74.457 23.543 74.6484 30.2422 73.4043 33.4961C76.4668 37.1328 78.0937 42.0137 78.0937 46.9902C78.0937 58.7617 69.1934 67.6621 56.3691 69.2891C59.623 71.3945 61.8242 75.9883 61.8242 81.252L61.8242 91.2051C61.8242 94.0762 64.2168 95.7031 67.0879 94.5547C84.4102 87.9512 98 70.6289 98 49.1914C98 22.1074 75.9883 6.69539e-07 48.9043 4.309e-07C21.8203 1.92261e-07 -1.9479e-07 22.1074 -4.3343e-07 49.1914C-6.20631e-07 70.4375 13.4941 88.0469 31.6777 94.6504C34.2617 95.6074 36.75 93.8848 36.75 91.3008L36.75 83.6445C35.4102 84.2188 33.6875 84.6016 32.1562 84.6016C25.8398 84.6016 22.1074 81.1563 19.4277 74.7441C18.375 72.1602 17.2266 70.6289 15.0254 70.3418C13.877 70.2461 13.4941 69.7676 13.4941 69.1934C13.4941 68.0449 15.4082 67.1836 17.3223 67.1836C20.0977 67.1836 22.4902 68.9063 24.9785 72.4473C26.8926 75.2227 28.9023 76.4668 31.2949 76.4668C33.6875 76.4668 35.2187 75.6055 37.4199 73.4043C39.0469 71.7773 40.291 70.3418 41.4395 69.3848Z"
          fill="#24292e"></path>
      </g>
      <defs>
        <clipPath id="clip0_730_27126">
          <rect width="98" height="96" fill="white"></rect>
        </clipPath>
      </defs>
    </svg>
  </a>

  <nav class="f4 list-style-none py-2 mt-2 mt-md-0">
    <a class="mr-3 mr-lg-4 py-2" href="https://help.github.com">Help</a>
    <a class="mr-3 mr-lg-4 py-2" href="https://github.community">Community</a>
    <a class="mr-3 py-2 text-gray " href="/">Status</a>
  </nav>

  <nav class="f4 list-style-none py-2 text-md-right">
    <a class="py-2" href="https://github.com">GitHub.com</a>
    <div class="d-inline py-2 ml-3 ml-lg-4">
      <div id="replace-with-subscribe"></div>
    </div>
  </nav>
</div>

<img src="https://user-images.githubusercontent.com/19292210/60553863-044dd200-9cea-11e9-987e-7db84449f215.png"
  class="illo-desktop-header" style="display: none;" alt="GitHub header">

<img src="https://user-images.githubusercontent.com/19292210/60553865-044dd200-9cea-11e9-859c-d6f266e2f01f.png"
  class="illo-mobile-header" alt="GitHub header">
      
  <div class="updates-dropdown-container" data-js-hook="updates-dropdown-container">
    <a href="#" data-js-hook="show-updates-dropdown" id="show-updates-dropdown" class="show-updates-dropdown" aria-label="Subscribe to updates" aria-expanded="false" aria-haspopup="dialog" role="button">
      <span class="subscribe-text-full">Subscribe to Updates</span><span class="subscribe-text-short">Subscribe</span>
    </a>

<!--    Accessibility guidelines for tabs: https://www.w3.org/TR/wai-aria-practices-1.1/examples/tabs/tabs-1/tabs.html -->
    <div class="updates-dropdown" data-js-hook="updates-dropdown" id="updates-dropdown" style="display:none" role="dialog" aria-modal="false" aria-label="Subscribe to updates">
      <div class="updates-dropdown-nav nav-items-7" role="tablist" aria-label="Subscribe to updates">
          <a href="#updates-dropdown-email" aria-controls="updates-dropdown-email" aria-label="Subscribe via email" role="tab" aria-selected="true" id="updates-dropdown-email-btn">
            <span class="icon-container email">
          </a>
          <a href="#updates-dropdown-sms" aria-controls="updates-dropdown-sms" aria-label="Subscribe via SMS" role="tab" id="updates-dropdown-sms-btn">
            <span class="icon-container sms">
          </a>
          <a href="#updates-dropdown-slack" aria-controls="updates-dropdown-slack" aria-label="Subscribe via slack" role="tab" id="updates-dropdown-slack-btn">
            <span class="icon-container slack">
          </a>
          <a href="#updates-dropdown-webhook" aria-controls="updates-dropdown-webhook" aria-label="Subscribe via webhook" role="tab" id="updates-dropdown-webhook-btn">
            <span class="icon-container webhook">
          </a>
          <a href="#updates-dropdown-support" aria-controls="updates-dropdown-support" aria-label="Contact support" role="tab" id="updates-dropdown-support-btn">
            <span class="icon-container support">
          </a>
          <a href="#updates-dropdown-atom" aria-controls="updates-dropdown-atom" aria-label="Subscribe via RSS" role="tab" id="updates-dropdown-atom-btn">
            <span class="icon-container rss">
          </a>
        <button data-js-hook="updates-dropdown-close" aria-label="Close subscribe form" id="updates-dropdown-close-btn">
          x
        </button>
      </div>
      <div class="updates-dropdown-sections-container">
          <div class="updates-dropdown-section email" id="updates-dropdown-email" style="display:none" role="tabpanel" aria-labelledby="updates-dropdown-email-btn">
            <div class="directions">
              Get email notifications whenever GitHub <strong>creates</strong>,  <strong>updates</strong> or <strong>resolves</strong> an incident.
            </div>
            <form id="subscribe-form-email" action="/subscriptions/new-email" accept-charset="UTF-8" data-remote="true" method="post">
              <input type="hidden" name="email_otp_verify_flow" id="email_otp_verify_flow" value="false" autocomplete="off" />
                <!-- make sure not to put cookie values in here since this gets cached -->
                <label for="email">Email address:</label>
                <input name="email" id="email" type="text" class="full-width" data-js-hook="email-notification-field" autocomplete="email">
                <input name="email_otp_auth_token" type='hidden' id="email-otp-token-field">
                <div class="opt-container-section" id="email-otp-container", style="display:none" >
                  <label for="email-otp">Enter OTP:</label>
                  <input name="otp" id="email-otp" type="text" value="" class="prepend full-width">
                  <p id="email-otp-timer">Resend OTP in: <span id="email-otp-countdown"></span> seconds </p>
                  <p id="resend-email-otp">
                    Didn't receive the OTP?
                    <a href="#" id="resend-email-otp-btn" >Resend OTP </a>
                  </p>
                </div>
                  <input type="hidden" name="captcha_error" id="captcha_error" value="false" autocomplete="off" />
                  <input type="submit" value="Subscribe via Email" class="flat-button full-width g-recaptcha" id="subscribe-btn-email" data-disabled-text="Subscribing..." data-sitekey=6LdTS8AUAAAAAOIbCKoCAP4LQku1olYGrywPTaZz data-callback="submitNewEmailSubscriber" data-error-callback="emailSubscriberCaptchaError" >
                  <div class="terms_and_privacy_information bottom small"><div class="privacy_policy_information small">By subscribing you agree to our <a target="_blank" rel="noopener" class="accessible-link" href="https://help.github.com/articles/github-privacy-statement/">Privacy Policy</a>.</div> This site is protected by reCAPTCHA and the Google <a target="_blank" rel="noopener" class="accessible-link" href="https://policies.google.com/privacy">Privacy Policy</a> and <a target="_blank" rel="noopener" class="accessible-link" data-js-hook="captcha-terms-of-service-link" href="https://policies.google.com/terms">Terms of Service</a> apply.</div>
</form>          </div>

          <div class="updates-dropdown-section phone" id="updates-dropdown-sms" style="display:none" role="tabpanel" aria-labelledby="updates-dropdown-sms-btn">
            <div class="directions">
                Get text message notifications whenever GitHub <strong>creates</strong> or <strong>resolves</strong> an incident.
            </div>
            <form id="subscribe-form-sms" action="/subscriptions/new-sms" accept-charset="UTF-8" data-remote="true" method="post">
              <input type="hidden" name="otp_verify_flow" id="otp_verify_flow" value="false" autocomplete="off" />
              <input type="hidden" name="subscriber_code" id="subscriber_code" value="" autocomplete="off" />
              <div class="control-group">
                <div class="controls externalities-sms-container">
                  <!-- make sure not to put cookie values in here since this gets cached -->
                  <label for="phone-country">Country code:</label>
                  <div id="phone-number-country-code" class="phone-country-wrapper"
                      data-otp-enabled="false">
                      <select name="phone_country" id="phone-country" data-js-hook="phone-country" class="phone-country"><option value="af" data-otp-enabled="false" >Afghanistan (+93)</option>
<option value="al" data-otp-enabled="false" >Albania (+355)</option>
<option value="dz" data-otp-enabled="false" >Algeria (+213)</option>
<option value="as" data-otp-enabled="false" >American Samoa (+1)</option>
<option value="ad" data-otp-enabled="false" >Andorra (+376)</option>
<option value="ao" data-otp-enabled="false" >Angola (+244)</option>
<option value="ai" data-otp-enabled="false" >Anguilla (+1)</option>
<option value="ag" data-otp-enabled="false" >Antigua and Barbuda (+1)</option>
<option value="ar" data-otp-enabled="false" >Argentina (+54)</option>
<option value="am" data-otp-enabled="false" >Armenia (+374)</option>
<option value="aw" data-otp-enabled="false" >Aruba (+297)</option>
<option value="au" data-otp-enabled="false" >Australia/Cocos/Christmas Island (+61)</option>
<option value="at" data-otp-enabled="false" >Austria (+43)</option>
<option value="az" data-otp-enabled="false" >Azerbaijan (+994)</option>
<option value="bs" data-otp-enabled="false" >Bahamas (+1)</option>
<option value="bh" data-otp-enabled="false" >Bahrain (+973)</option>
<option value="bd" data-otp-enabled="false" >Bangladesh (+880)</option>
<option value="bb" data-otp-enabled="false" >Barbados (+1)</option>
<option value="by" data-otp-enabled="false" >Belarus (+375)</option>
<option value="be" data-otp-enabled="false" >Belgium (+32)</option>
<option value="bz" data-otp-enabled="false" >Belize (+501)</option>
<option value="bj" data-otp-enabled="false" >Benin (+229)</option>
<option value="bm" data-otp-enabled="false" >Bermuda (+1)</option>
<option value="bo" data-otp-enabled="false" >Bolivia (+591)</option>
<option value="ba" data-otp-enabled="false" >Bosnia and Herzegovina (+387)</option>
<option value="bw" data-otp-enabled="false" >Botswana (+267)</option>
<option value="br" data-otp-enabled="false" >Brazil (+55)</option>
<option value="bn" data-otp-enabled="false" >Brunei (+673)</option>
<option value="bg" data-otp-enabled="false" >Bulgaria (+359)</option>
<option value="bf" data-otp-enabled="false" >Burkina Faso (+226)</option>
<option value="bi" data-otp-enabled="false" >Burundi (+257)</option>
<option value="kh" data-otp-enabled="false" >Cambodia (+855)</option>
<option value="cm" data-otp-enabled="false" >Cameroon (+237)</option>
<option value="ca" data-otp-enabled="false" >Canada (+1)</option>
<option value="cv" data-otp-enabled="false" >Cape Verde (+238)</option>
<option value="ky" data-otp-enabled="false" >Cayman Islands (+1)</option>
<option value="cf" data-otp-enabled="false" >Central Africa (+236)</option>
<option value="td" data-otp-enabled="false" >Chad (+235)</option>
<option value="cl" data-otp-enabled="false" >Chile (+56)</option>
<option value="cn" data-otp-enabled="false" >China (+86)</option>
<option value="co" data-otp-enabled="false" >Colombia (+57)</option>
<option value="km" data-otp-enabled="false" >Comoros (+269)</option>
<option value="cg" data-otp-enabled="false" >Congo (+242)</option>
<option value="cd" data-otp-enabled="false" >Congo, Dem Rep (+243)</option>
<option value="cr" data-otp-enabled="false" >Costa Rica (+506)</option>
<option value="hr" data-otp-enabled="false" >Croatia (+385)</option>
<option value="cy" data-otp-enabled="false" >Cyprus (+357)</option>
<option value="cz" data-otp-enabled="false" >Czech Republic (+420)</option>
<option value="dk" data-otp-enabled="false" >Denmark (+45)</option>
<option value="dj" data-otp-enabled="false" >Djibouti (+253)</option>
<option value="dm" data-otp-enabled="false" >Dominica (+1)</option>
<option value="do" data-otp-enabled="false" >Dominican Republic (+1)</option>
<option value="eg" data-otp-enabled="false" >Egypt (+20)</option>
<option value="sv" data-otp-enabled="false" >El Salvador (+503)</option>
<option value="gq" data-otp-enabled="false" >Equatorial Guinea (+240)</option>
<option value="ee" data-otp-enabled="false" >Estonia (+372)</option>
<option value="et" data-otp-enabled="false" >Ethiopia (+251)</option>
<option value="fo" data-otp-enabled="false" >Faroe Islands (+298)</option>
<option value="fj" data-otp-enabled="false" >Fiji (+679)</option>
<option value="fi" data-otp-enabled="false" >Finland/Aland Islands (+358)</option>
<option value="fr" data-otp-enabled="false" >France (+33)</option>
<option value="gf" data-otp-enabled="false" >French Guiana (+594)</option>
<option value="pf" data-otp-enabled="false" >French Polynesia (+689)</option>
<option value="ga" data-otp-enabled="false" >Gabon (+241)</option>
<option value="gm" data-otp-enabled="false" >Gambia (+220)</option>
<option value="ge" data-otp-enabled="false" >Georgia (+995)</option>
<option value="de" data-otp-enabled="false" >Germany (+49)</option>
<option value="gh" data-otp-enabled="false" >Ghana (+233)</option>
<option value="gi" data-otp-enabled="false" >Gibraltar (+350)</option>
<option value="gr" data-otp-enabled="false" >Greece (+30)</option>
<option value="gl" data-otp-enabled="false" >Greenland (+299)</option>
<option value="gd" data-otp-enabled="false" >Grenada (+1)</option>
<option value="gp" data-otp-enabled="false" >Guadeloupe (+590)</option>
<option value="gu" data-otp-enabled="false" >Guam (+1)</option>
<option value="gt" data-otp-enabled="false" >Guatemala (+502)</option>
<option value="gn" data-otp-enabled="false" >Guinea (+224)</option>
<option value="gy" data-otp-enabled="false" >Guyana (+592)</option>
<option value="ht" data-otp-enabled="false" >Haiti (+509)</option>
<option value="hn" data-otp-enabled="false" >Honduras (+504)</option>
<option value="hk" data-otp-enabled="false" >Hong Kong (+852)</option>
<option value="hu" data-otp-enabled="false" >Hungary (+36)</option>
<option value="is" data-otp-enabled="false" >Iceland (+354)</option>
<option value="in" data-otp-enabled="false" >India (+91)</option>
<option value="id" data-otp-enabled="false" >Indonesia (+62)</option>
<option value="iq" data-otp-enabled="false" >Iraq (+964)</option>
<option value="ie" data-otp-enabled="false" >Ireland (+353)</option>
<option value="il" data-otp-enabled="false" >Israel (+972)</option>
<option value="it" data-otp-enabled="false" >Italy (+39)</option>
<option value="jm" data-otp-enabled="false" >Jamaica (+1)</option>
<option value="jp" data-otp-enabled="false" >Japan (+81)</option>
<option value="jo" data-otp-enabled="false" >Jordan (+962)</option>
<option value="ke" data-otp-enabled="false" >Kenya (+254)</option>
<option value="kr" data-otp-enabled="false" >Korea, Republic of (+82)</option>
<option value="xk" data-otp-enabled="false" >Kosovo (+383)</option>
<option value="kw" data-otp-enabled="false" >Kuwait (+965)</option>
<option value="kg" data-otp-enabled="false" >Kyrgyzstan (+996)</option>
<option value="la" data-otp-enabled="false" >Laos (+856)</option>
<option value="lv" data-otp-enabled="false" >Latvia (+371)</option>
<option value="lb" data-otp-enabled="false" >Lebanon (+961)</option>
<option value="ls" data-otp-enabled="false" >Lesotho (+266)</option>
<option value="lr" data-otp-enabled="false" >Liberia (+231)</option>
<option value="ly" data-otp-enabled="false" >Libya (+218)</option>
<option value="li" data-otp-enabled="false" >Liechtenstein (+423)</option>
<option value="lt" data-otp-enabled="false" >Lithuania (+370)</option>
<option value="lu" data-otp-enabled="false" >Luxembourg (+352)</option>
<option value="mo" data-otp-enabled="false" >Macao (+853)</option>
<option value="mk" data-otp-enabled="false" >Macedonia (+389)</option>
<option value="mg" data-otp-enabled="false" >Madagascar (+261)</option>
<option value="mw" data-otp-enabled="false" >Malawi (+265)</option>
<option value="my" data-otp-enabled="false" >Malaysia (+60)</option>
<option value="mv" data-otp-enabled="false" >Maldives (+960)</option>
<option value="ml" data-otp-enabled="false" >Mali (+223)</option>
<option value="mt" data-otp-enabled="false" >Malta (+356)</option>
<option value="mq" data-otp-enabled="false" >Martinique (+596)</option>
<option value="mr" data-otp-enabled="false" >Mauritania (+222)</option>
<option value="mu" data-otp-enabled="false" >Mauritius (+230)</option>
<option value="mx" data-otp-enabled="false" >Mexico (+52)</option>
<option value="mc" data-otp-enabled="false" >Monaco (+377)</option>
<option value="mn" data-otp-enabled="false" >Mongolia (+976)</option>
<option value="me" data-otp-enabled="false" >Montenegro (+382)</option>
<option value="ms" data-otp-enabled="false" >Montserrat (+1)</option>
<option value="ma" data-otp-enabled="false" >Morocco/Western Sahara (+212)</option>
<option value="mz" data-otp-enabled="false" >Mozambique (+258)</option>
<option value="na" data-otp-enabled="false" >Namibia (+264)</option>
<option value="np" data-otp-enabled="false" >Nepal (+977)</option>
<option value="nl" data-otp-enabled="false" >Netherlands (+31)</option>
<option value="nz" data-otp-enabled="false" >New Zealand (+64)</option>
<option value="ni" data-otp-enabled="false" >Nicaragua (+505)</option>
<option value="ne" data-otp-enabled="false" >Niger (+227)</option>
<option value="ng" data-otp-enabled="false" >Nigeria (+234)</option>
<option value="no" data-otp-enabled="false" >Norway (+47)</option>
<option value="om" data-otp-enabled="false" >Oman (+968)</option>
<option value="pk" data-otp-enabled="false" >Pakistan (+92)</option>
<option value="ps" data-otp-enabled="false" >Palestinian Territory (+970)</option>
<option value="pa" data-otp-enabled="false" >Panama (+507)</option>
<option value="py" data-otp-enabled="false" >Paraguay (+595)</option>
<option value="pe" data-otp-enabled="false" >Peru (+51)</option>
<option value="ph" data-otp-enabled="false" >Philippines (+63)</option>
<option value="pl" data-otp-enabled="false" >Poland (+48)</option>
<option value="pt" data-otp-enabled="false" >Portugal (+351)</option>
<option value="pr" data-otp-enabled="false" >Puerto Rico (+1)</option>
<option value="qa" data-otp-enabled="false" >Qatar (+974)</option>
<option value="re" data-otp-enabled="false" >Reunion/Mayotte (+262)</option>
<option value="ro" data-otp-enabled="false" >Romania (+40)</option>
<option value="ru" data-otp-enabled="false" >Russia/Kazakhstan (+7)</option>
<option value="rw" data-otp-enabled="false" >Rwanda (+250)</option>
<option value="ws" data-otp-enabled="false" >Samoa (+685)</option>
<option value="sm" data-otp-enabled="false" >San Marino (+378)</option>
<option value="sa" data-otp-enabled="false" >Saudi Arabia (+966)</option>
<option value="sn" data-otp-enabled="false" >Senegal (+221)</option>
<option value="rs" data-otp-enabled="false" >Serbia (+381)</option>
<option value="sc" data-otp-enabled="false" >Seychelles (+248)</option>
<option value="sl" data-otp-enabled="false" >Sierra Leone (+232)</option>
<option value="sg" data-otp-enabled="false" >Singapore (+65)</option>
<option value="sk" data-otp-enabled="false" >Slovakia (+421)</option>
<option value="si" data-otp-enabled="false" >Slovenia (+386)</option>
<option value="za" data-otp-enabled="false" >South Africa (+27)</option>
<option value="es" data-otp-enabled="false" >Spain (+34)</option>
<option value="lk" data-otp-enabled="false" >Sri Lanka (+94)</option>
<option value="kn" data-otp-enabled="false" >St Kitts and Nevis (+1)</option>
<option value="lc" data-otp-enabled="false" >St Lucia (+1)</option>
<option value="vc" data-otp-enabled="false" >St Vincent Grenadines (+1)</option>
<option value="sd" data-otp-enabled="false" >Sudan (+249)</option>
<option value="sr" data-otp-enabled="false" >Suriname (+597)</option>
<option value="sz" data-otp-enabled="false" >Swaziland (+268)</option>
<option value="se" data-otp-enabled="false" >Sweden (+46)</option>
<option value="ch" data-otp-enabled="false" >Switzerland (+41)</option>
<option value="tw" data-otp-enabled="false" >Taiwan (+886)</option>
<option value="tj" data-otp-enabled="false" >Tajikistan (+992)</option>
<option value="tz" data-otp-enabled="false" >Tanzania (+255)</option>
<option value="th" data-otp-enabled="false" >Thailand (+66)</option>
<option value="tg" data-otp-enabled="false" >Togo (+228)</option>
<option value="to" data-otp-enabled="false" >Tonga (+676)</option>
<option value="tt" data-otp-enabled="false" >Trinidad and Tobago (+1)</option>
<option value="tn" data-otp-enabled="false" >Tunisia (+216)</option>
<option value="tr" data-otp-enabled="false" >Turkey (+90)</option>
<option value="tc" data-otp-enabled="false" >Turks and Caicos Islands (+1)</option>
<option value="ug" data-otp-enabled="false" >Uganda (+256)</option>
<option value="ua" data-otp-enabled="false" >Ukraine (+380)</option>
<option value="ae" data-otp-enabled="false" >United Arab Emirates (+971)</option>
<option value="gb" data-otp-enabled="false" >United Kingdom (+44)</option>
<option value="us" data-otp-enabled="false" selected>United States (+1)</option>
<option value="uy" data-otp-enabled="false" >Uruguay (+598)</option>
<option value="uz" data-otp-enabled="false" >Uzbekistan (+998)</option>
<option value="ve" data-otp-enabled="false" >Venezuela (+58)</option>
<option value="vn" data-otp-enabled="false" >Vietnam (+84)</option>
<option value="vg" data-otp-enabled="false" >Virgin Islands, British (+1)</option>
<option value="vi" data-otp-enabled="false" >Virgin Islands, U.S. (+1)</option>
<option value="ye" data-otp-enabled="false" >Yemen (+967)</option>
<option value="zm" data-otp-enabled="false" >Zambia (+260)</option>
<option value="zw" data-otp-enabled="false" >Zimbabwe (+263)</option></select>
                  </div>
                  <label for="phone-number">Phone number:</label>
                  <input name="phone_number" id="phone-number" type="text" class="prepend full-width" data-js-hook="sms-notification-field">
                  <div class="sms-atl-error" id="sms-atl-error"></div>
                  <div class="clearfix"></div>
                  <div class="opt-container-section" id="otp-container" style="display:none">
                    <a href="#" id="btn-subcriber-change-number">Change number</a>
                    <label for="otp">Enter OTP:</label>
                    <input name="otp" id="otp" type="text" class="prepend full-width">
                    <p id="timer">Resend OTP in: <span id="countdown">30</span> seconds </p>
                    <p id="resend">
                      Didn't receive the OTP?
                      <a href="#" id="resend-otp-btn" >Resend OTP </a>
                    </p>
                    </div>
                </div>
              </div>

                <input type="hidden" name="captcha_error" id="captcha_error" value="false" autocomplete="off" />
                <input type="submit" value="Subscribe via Text Message" class="flat-button full-width g-recaptcha" id="subscribe-btn-sms" data-disabled-text="Subscribing..." data-sitekey=6LcH-b0UAAAAACVQtMb14LBhflMA9y0Nmu7l_W6d data-callback="submitNewSmsSubscriber" data-error-callback="smsSubscriberCaptchaError">
              <div class="terms_and_privacy_information bottom small">Message and data rates may apply. By subscribing you agree to our <a target="_blank" rel="noopener" class="accessible-link" href="https://help.github.com/articles/github-privacy-statement/">Privacy Policy</a>, the Atlassian <a target="_blank" rel="noopener" class="accessible-link" href="https://www.atlassian.com/legal/product-specific-terms#statuspage-specific-terms">Terms of Service</a>, and the Atlassian <a target="_blank" rel="noopener" class="accessible-link" href="https://www.atlassian.com/legal/privacy-policy">Privacy Policy</a>. This site is protected by reCAPTCHA and the Google <a target="_blank" rel="noopener" class="accessible-link" href="https://policies.google.com/privacy">Privacy Policy</a> and <a target="_blank" rel="noopener" class="accessible-link" data-js-hook="captcha-terms-of-service-link" href="https://policies.google.com/terms">Terms of Service</a> apply.</div>
</form>          </div>

          <div class="updates-dropdown-section slack" id="updates-dropdown-slack" style="display:none" role="tabpanel" aria-labelledby="updates-dropdown-slack-btn">
            <div class="directions">
              Get incident updates and maintenance status messages in Slack.
            </div>
            <a value="Subscribe via Slack" class="flat-button full-width" id="subscribe-btn-slack" data-disabled-text="Subscribing..." data-revert-on-success="true" style="margin-top:.75rem" href="https://subscriptions.statuspage.io/slack_authentication/kickoff?page_code=kctbh9vrtdwd">Subscribe via Slack</a>
            <div class="terms_and_privacy_information bottom small">By subscribing you acknowledge our <a target="_blank" rel="noopener" class="accessible-link" href="https://help.github.com/articles/github-privacy-statement/">Privacy Policy</a>. In addition, you agree to the Atlassian <a target="_blank" rel="noopener" class="accessible-link" href="https://www.atlassian.com/legal/cloud-terms-of-service">Cloud Terms of Service</a> and acknowledge Atlassian's <a target="_blank" rel="noopener" class="accessible-link" href="https://www.atlassian.com/legal/privacy-policy">Privacy Policy</a>.</div>
          </div>


          <div class="updates-dropdown-section webhook" id="updates-dropdown-webhook" style="display:none" role="tabpanel" aria-labelledby="updates-dropdown-webhook-btn">
            <div class="directions">
              Get webhook notifications whenever GitHub <strong>creates</strong> an incident, <strong>updates</strong> an incident, <strong>resolves</strong> an incident or <strong>changes</strong> a component status.
            </div>
            <form id="subscribe-form-webhook" action="/subscriptions/webhook.json" accept-charset="UTF-8" data-remote="true" method="post">
              <div class="control-group">
                <div class="controls">
                  <label for="endpoint-webhooks">Webhook URL:</label>
                  <input type="text" name="endpoint" id="endpoint-webhooks" data-js-hook="endpoint" class="full-width" aria-describedby="url-help-block" />
                  <p class="help-block" id="url-help-block">The URL we should send the webhooks to</p>
                </div>
              </div>

              <div class="control-group">
                <div class="controls">
                  <label for="email-webhooks">Email address:</label>
                  <input type="text" name="email" id="email-webhooks" data-js-hook="email" class="full-width" aria-describedby="email-help-block" />
                  <p class="help-block" id="email-help-block">We'll send you email if your endpoint fails</p>
                </div>
              </div>

                <input type="hidden" name="captcha_error" id="captcha_error" value="false" autocomplete="off" />
                <input type="submit" value=Subscribe To Notifications class="flat-button full-width g-recaptcha" id="subscribe-btn-webhook" data-disabled-text="Subscribing..." data-sitekey=6LcQ-b0UAAAAAJjfdwO_-ozGC-CzWDj4Pm1kJ2Ah data-callback="submitNewWebhookSubscriber" data-error-callback="webhookSubscriberCaptchaError">
                <div class="terms_and_privacy_information bottom small"><div class="privacy_policy_information small">By subscribing you agree to our <a target="_blank" rel="noopener" class="accessible-link" href="https://help.github.com/articles/github-privacy-statement/">Privacy Policy</a>.</div> This site is protected by reCAPTCHA and the Google <a target="_blank" rel="noopener" class="accessible-link" href="https://policies.google.com/privacy">Privacy Policy</a> and <a target="_blank" rel="noopener" class="accessible-link" data-js-hook="captcha-terms-of-service-link" href="https://policies.google.com/terms">Terms of Service</a> apply.</div>

</form>          </div>


          <div class="updates-dropdown-section support" id="updates-dropdown-support" style="display:none" role="tabpanel" aria-labelledby="updates-dropdown-support-btn">
            Visit our <a target="_blank" href="https://github.com/support">support site</a>.
          </div>

          <div class="updates-dropdown-section atom" id="updates-dropdown-atom" role="tabpanel" aria-labelledby="updates-dropdown-atom-btn">
            Get the <a href="https://www.githubstatus.com/history.atom" target="_blank">Atom Feed</a> or <a href="https://www.githubstatus.com/history.rss" target="_blank">RSS Feed</a>.
          </div>
      </div>
    </div>
  </div>

<script>
  $(function () {
    const phoneNumberInput = $('#phone-number');
    const errorDiv = $('#sms-atl-error')
    if(errorDiv.length){
      function checkSelectedCountry() {
        const selectedCountry = $('#phone-country').val();
        const isOtpEnabled = $('#phone-number-country-code').attr('data-otp-enabled') === 'true';
        const form = document.getElementById('subscribe-form-sms');
        form.action = '/subscriptions/new-sms';
        const isOtpFlow = document.getElementById('otp_verify_flow');
        document.getElementById('otp-container').style.display = "none";
        if(false && selectedCountry === 'sg') { // Replace 'SG' with the actual value representing Singapore in your select tag
          phoneNumberInput.prop('disabled', true);
          errorDiv.html(`Due to new Singapore government regulations, we're currently not supporting text subscriptions in Singapore.<a href="https://community.atlassian.com/t5/Statuspage-articles/Attention-SMS-notifications-will-be-disabled-on-August-1st-2023/ba-p/2424398" target="_blank"> Learn more.</a> <br> Select another method to subscribe.`);
        } else {
          phoneNumberInput.prop('readonly', false);
          errorDiv.html('');
          if(false){
            if(isOtpEnabled){
              document.getElementById('subscribe-btn-sms').value = "Send OTP";
            }
            else {
              isOtpFlow.value = false;
              document.getElementById('subscribe-btn-sms').value = "Subscribe via Text Message";
            }
          }
        }
      }

      $('#phone-country').on('change', checkSelectedCountry);
      checkSelectedCountry();
    }
  });

  document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.querySelector('#phone-number-country-code .phone-country');
    if (dropdown){
      const wrapperDiv = document.getElementById('phone-number-country-code');
      const selectedOption = dropdown.options[dropdown.selectedIndex];
      const otpEnabled = selectedOption.getAttribute('data-otp-enabled');

      wrapperDiv.setAttribute('data-otp-enabled', otpEnabled);

      dropdown.addEventListener('change', function() {
        const selectedOption = dropdown.options[dropdown.selectedIndex];
        const otpEnabled = selectedOption.getAttribute('data-otp-enabled');

        wrapperDiv.setAttribute('data-otp-enabled', otpEnabled);
      });
    }
  });

  var countdownTimer;
  var resendBtn = document.getElementById('resend');
  var timer = document.getElementById('timer');
  var form = document.getElementById('subscribe-form-sms');
  var RESEND_TIMER = 30;
  $(function() {
    $('#subscribe-form-sms').on('ajax:success', function(e, data, status, xhr){
      const form = this;
      const action = form.getAttribute('action');
      if (data.type === 'success' && data.otp_flow === true) {
        document.getElementById('subscriber_code').value = data.subscriber_code
        document.getElementById('otp-container').style.display = "block";
        $('#phone-number').prop('readonly', true);
        var display = document.getElementById('countdown');
        disableResend();
        startTimer(RESEND_TIMER, display)
        document.getElementById('subscribe-btn-sms').value = "Verify OTP and Subscribe";
        document.getElementById('otp_verify_flow').value = true;
        form.action = '/subscriptions/verify-otp';
      } else if (data.type === 'success' && action.includes('verify')){
        document.getElementById('otp-container').style.display = "none";
        $('#phone-number').val('').prop('readonly', false);
        $('#otp').val('');
        document.getElementById('subscribe-btn-sms').value = "Send OTP";
        document.getElementById('otp_verify_flow').value = false;
        form.action = '/subscriptions/new-sms';
        SP.currentPage.updatesDropdown.hide();
      }
    });
    $("#btn-subcriber-change-number").on('click', () => {
      document.getElementById('otp-container').style.display = "none";
      $('#phone-number').prop('readonly', false);
      document.getElementById('subscribe-btn-sms').value = "Send OTP";
      form.action = '/subscriptions/new-sms';
      return false
    })
    $('#resend-otp-btn').on('click', function(e) {
      e.preventDefault();
      let phoneNumber = $('#phone-number').val();
      let countryCode = $('.phone-country').val();
      $.ajax({
        type: 'POST',
        url: "/subscriptions/new-sms",
        data: {
          phone_number: phoneNumber,
          phone_country: countryCode,
          type: 'resend'
        },
      }).done(function(data) {
        var messageOptions = (data.type !== undefined && data.type !== null) ? { cssClass: data.type } : {};
        HRB.utils.notify(data.text, messageOptions);
        var display = document.getElementById('countdown');
        disableResend();
        timer.style.display = "none"
        if (data.type === 'success') {
          startTimer(RESEND_TIMER, display);
        }
      })
    });
  })

  function startTimer(duration, display){
    var timer = duration, seconds;
    clearInterval(countdownTimer);
    countdownTimer = setInterval(function () {
      seconds = parseInt(timer % 60, 10);
      display.textContent = seconds;
      if(--timer < 0){
        enableResend();
        clearInterval(countdownTimer);
      }
    }, 1000);
    disableResend();
  }
  function enableResend(){
    resendBtn.style.display = "block";
    timer.style.display = "none"
  }
  function disableResend(){
    resendBtn.style.display = "none";
    timer.style.display = "block"
  }

  $(function() {
    $('#subscribe-form-email').on('submit', function() {
      var tokenField = document.getElementById('email-otp-token-field');
      if (!tokenField) {
        return;
      }
      let page_code = "kctbh9vrtdwd"
      let key = keyForEmailOtpToken($('#email').val(), page_code);
      tokenField.value = localStorage.getItem(key);
    });
  });

  var emailOtpCountdownTimer;
  var emailOtpResendBtn = document.getElementById('resend-email-otp');
  var emailOtpTimer = document.getElementById('email-otp-timer');
  var emailOtpForm = document.getElementById('subscribe-form-email');
  var EMAIL_OTP_RESEND_TIMER = 600;
  $(function() {
    $('#subscribe-form-email').on('ajax:success', function(e, data, status, xhr){
      const form = this;
      const action = form.getAttribute('action');
      if (data.type === 'success' && data.email_otp_verify_flow === true) {
        document.getElementById('email-otp-container').style.display = "block";
        var display = document.getElementById('email-otp-countdown');
        display.textContent = EMAIL_OTP_RESEND_TIMER;
        disableEmailOtpResend();
        startEmailOtpTimer(EMAIL_OTP_RESEND_TIMER, display)
        document.getElementById('subscribe-btn-email').value = "Verify OTP and Subscribe";
        document.getElementById('email_otp_verify_flow').value = true;
        form.action = '/subscriptions/verify-email-otp';
      } else if (data.type === 'success' && action.includes('verify')){
        let email =  $('#email')
        let page_code = "kctbh9vrtdwd"
        let key = keyForEmailOtpToken(email.val(), page_code);
        localStorage.setItem(key, data.email_otp_auth_token);

        document.getElementById('email-otp-container').style.display = "none";
        email.val('').prop('readonly', false);
        $('#email-otp').val('');
        document.getElementById('subscribe-btn-email').value = "Send OTP";
        document.getElementById('email_otp_verify_flow').value = false;
        form.action = '/subscriptions/new-email';
        SP.currentPage.updatesDropdown.hide();
      }
    });
    $('#resend-email-otp-btn').on('click', function(e) {
      e.preventDefault();
      let email = $('#email').val();
      $.ajax({
        type: 'POST',
        url: "/subscriptions/new-email",
        data: {
          email: email
        },
      }).done(function(data) {
        var messageOptions = (data.type !== undefined && data.type !== null) ? { cssClass: data.type } : {};
        HRB.utils.notify(data.text, messageOptions);
        if (data.type === 'success') {
          var display = document.getElementById('email-otp-countdown');
          display.textContent = EMAIL_OTP_RESEND_TIMER;
          disableEmailOtpResend();
          emailOtpTimer.style.display = "none"
          startEmailOtpTimer(EMAIL_OTP_RESEND_TIMER, display);
        }
      })
    });
  })

  function startEmailOtpTimer(duration, display){
    var timer = duration, seconds;
    clearInterval(emailOtpCountdownTimer);
    emailOtpCountdownTimer = setInterval(function () {
      seconds = parseInt(timer, 10);
      display.textContent = seconds;
      if(--timer < 0){
        enableEmailOtpResend();
        clearInterval(emailOtpCountdownTimer);
      }
    }, 1000);
    disableEmailOtpResend();
  }

  function enableEmailOtpResend(){
    emailOtpResendBtn.style.display = "block";
    emailOtpTimer.style.display = "none"
  }
  function disableEmailOtpResend(){
    emailOtpResendBtn.style.display = "none";
    emailOtpTimer.style.display = "block"
  }
  function keyForEmailOtpToken(email, pageCode) {
    return email + '|' + pageCode+ '|SUBSCRIBE_VIA_EMAIL';
  }
</script>

  </div>


  <div class="container">
      <div class="history-nav border-color">
  <ul>
    <li>
      <a class="button current border-color"  href="https://www.githubstatus.com/history" aria-label="Incidents" aria-current=page>Incidents</a>
    </li>
    <li>
      <a class="button border-color" href="https://www.githubstatus.com/uptime" aria-label="Uptime" >Uptime</a>
    </li>
  </ul>
</div>


    <div data-react-class="HistoryIndex" data-react-props="{&quot;page_status&quot;:{&quot;page&quot;:{&quot;name&quot;:&quot;GitHub&quot;,&quot;subdomain&quot;:&quot;github3&quot;,&quot;domain&quot;:&quot;www.githubstatus.com&quot;,&quot;created_at&quot;:&quot;2017-01-31T20:01:46.612Z&quot;,&quot;updated_at&quot;:&quot;2026-08-28T01:45:26.822Z&quot;,&quot;url&quot;:&quot;https://github.com&quot;,&quot;hidden_from_search&quot;:false,&quot;css_body_background_color&quot;:&quot;ffffff&quot;,&quot;css_font_color&quot;:&quot;24292e&quot;,&quot;css_light_font_color&quot;:&quot;6a737d&quot;,&quot;css_greens&quot;:&quot;28a745&quot;,&quot;css_yellows&quot;:&quot;dbab09&quot;,&quot;css_oranges&quot;:&quot;e36209&quot;,&quot;css_reds&quot;:&quot;dc3545&quot;,&quot;allow_page_subscribers&quot;:true,&quot;allow_incident_subscribers&quot;:true,&quot;notifications_from_email&quot;:&quot;GitHub Status \u003cnoreply@githubstatus.com\u003e&quot;,&quot;allow_email_subscribers&quot;:true,&quot;allow_sms_subscribers&quot;:true,&quot;twitter_username&quot;:null,&quot;branding&quot;:&quot;basic&quot;,&quot;support_url&quot;:&quot;https://github.com/support&quot;,&quot;allow_webhook_subscribers&quot;:true,&quot;css_border_color&quot;:&quot;e1e4e8&quot;,&quot;css_graph_color&quot;:&quot;0366d6&quot;,&quot;css_link_color&quot;:&quot;0366d6&quot;,&quot;page_description&quot;:&quot;Check GitHub Enterprise Cloud status by region:\r\n- Australia: \u003ca href=\&quot;https://au.githubstatus.com\&quot;\u003eau.githubstatus.com\u003c/a\u003e\r\n- EU: \u003ca href=\&quot;https://eu.githubstatus.com\&quot;\u003eeu.githubstatus.com\u003c/a\u003e\r\n- Japan: \u003ca href=\&quot;https://jp.githubstatus.com\&quot;\u003ejp.githubstatus.com\u003c/a\u003e\r\n- US: \u003ca href=\&quot;https://us.githubstatus.com/\&quot;\u003eus.githubstatus.com\u003c/a\u003e&quot;,&quot;activity_score&quot;:3939,&quot;headline&quot;:null,&quot;viewers_must_be_team_members&quot;:false,&quot;ip_filters&quot;:null,&quot;css_blues&quot;:&quot;0366d6&quot;,&quot;time_zone&quot;:&quot;UTC&quot;,&quot;notifications_reply_to_email&quot;:null,&quot;notifications_email_footer&quot;:&quot;You received this email because you are subscribed to GitHub&#39;s service status notifications.&quot;,&quot;allow_rss_atom_feeds&quot;:true,&quot;black_hole&quot;:null,&quot;over_allocations_cohort&quot;:null,&quot;over_allocations_resolved_at&quot;:null,&quot;custom_components_limit&quot;:null,&quot;allow_slack_subscribers&quot;:true,&quot;css_no_data&quot;:&quot;b3bac5&quot;,&quot;deleted_at&quot;:null,&quot;allow_teams_subscription&quot;:false,&quot;max_maintenance_automation_allowed&quot;:null,&quot;custom_email_template&quot;:false,&quot;hero_cover&quot;:{&quot;updated_at&quot;:null,&quot;original_url&quot;:&quot;&quot;,&quot;size&quot;:null,&quot;normal_url&quot;:&quot;&quot;,&quot;retina_url&quot;:&quot;&quot;},&quot;transactional_logo&quot;:{&quot;updated_at&quot;:&quot;2018-02-05T16:24:16.000+00:00&quot;,&quot;original_url&quot;:&quot;//dka575ofm4ao0.cloudfront.net/pages-transactional_logos/original/36420/hTgCmUjbT7WMYBbAnxDp&quot;,&quot;size&quot;:7056,&quot;normal_url&quot;:&quot;//dka575ofm4ao0.cloudfront.net/pages-transactional_logos/normal/36420/hTgCmUjbT7WMYBbAnxDp&quot;,&quot;retina_url&quot;:&quot;//dka575ofm4ao0.cloudfront.net/pages-transactional_logos/retina/36420/hTgCmUjbT7WMYBbAnxDp&quot;},&quot;favicon_logo&quot;:{&quot;updated_at&quot;:&quot;2018-01-17T23:38:34.000+00:00&quot;,&quot;size&quot;:6518,&quot;url&quot;:&quot;//dka575ofm4ao0.cloudfront.net/pages-favicon_logos/original/36420/akacZEQQfOBdc7ftyxJt&quot;},&quot;email_logo&quot;:{&quot;updated_at&quot;:null,&quot;original_url&quot;:&quot;&quot;,&quot;size&quot;:null,&quot;normal_url&quot;:&quot;&quot;,&quot;retina_url&quot;:&quot;&quot;},&quot;twitter_logo&quot;:{&quot;updated_at&quot;:&quot;2019-01-10T19:02:40.000+00:00&quot;,&quot;size&quot;:4268,&quot;url&quot;:&quot;//dka575ofm4ao0.cloudfront.net/pages-twitter_logos/original/36420/GitHub-Mark-120px-plus.png&quot;},&quot;id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;organization_id&quot;:&quot;30gcnw2xxnb0&quot;}},&quot;components&quot;:[{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Git Operations&quot;,&quot;created_at&quot;:&quot;2017-01-31T20:05:05.370Z&quot;,&quot;updated_at&quot;:&quot;2026-08-17T18:23:47.907Z&quot;,&quot;position&quot;:1,&quot;description&quot;:&quot;Performance of git clones, pulls, pushes, and associated operations&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;8l4ygp009s5s&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Webhooks&quot;,&quot;created_at&quot;:&quot;2019-11-13T18:00:24.256Z&quot;,&quot;updated_at&quot;:&quot;2026-08-17T16:59:38.017Z&quot;,&quot;position&quot;:2,&quot;description&quot;:&quot;Real time HTTP callbacks of user-generated and system events&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;4230lsnqdsld&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Visit www.githubstatus.com for more information&quot;,&quot;created_at&quot;:&quot;2018-12-05T19:39:40.838Z&quot;,&quot;updated_at&quot;:&quot;2025-03-19T05:00:21.309Z&quot;,&quot;position&quot;:3,&quot;description&quot;:null,&quot;showcase&quot;:false,&quot;start_date&quot;:null,&quot;id&quot;:&quot;0l2p9nhqnxpd&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;API Requests&quot;,&quot;created_at&quot;:&quot;2017-01-31T20:01:46.621Z&quot;,&quot;updated_at&quot;:&quot;2026-08-17T19:01:45.543Z&quot;,&quot;position&quot;:4,&quot;description&quot;:&quot;Requests for GitHub APIs&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;brv1bkgrwx7q&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Issues&quot;,&quot;created_at&quot;:&quot;2017-01-31T20:01:46.638Z&quot;,&quot;updated_at&quot;:&quot;2026-08-17T20:22:28.767Z&quot;,&quot;position&quot;:5,&quot;description&quot;:&quot;Requests for Issues on GitHub.com&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;kr09ddfgbfsf&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Pull Requests&quot;,&quot;created_at&quot;:&quot;2020-09-02T15:39:06.329Z&quot;,&quot;updated_at&quot;:&quot;2026-08-27T00:26:05.938Z&quot;,&quot;position&quot;:6,&quot;description&quot;:&quot;Requests for Pull Requests on GitHub.com&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;hhtssxt0f5v2&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Actions&quot;,&quot;created_at&quot;:&quot;2019-11-13T18:02:19.432Z&quot;,&quot;updated_at&quot;:&quot;2026-08-27T00:26:05.957Z&quot;,&quot;position&quot;:7,&quot;description&quot;:&quot;Workflows, Compute and Orchestration for GitHub Actions&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;br0l2tvcx85d&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Packages&quot;,&quot;created_at&quot;:&quot;2019-11-13T18:02:40.064Z&quot;,&quot;updated_at&quot;:&quot;2026-08-13T15:33:02.208Z&quot;,&quot;position&quot;:8,&quot;description&quot;:&quot;API requests and webhook delivery for GitHub Packages&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;st3j38cctv9l&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Pages&quot;,&quot;created_at&quot;:&quot;2017-01-31T20:04:33.923Z&quot;,&quot;updated_at&quot;:&quot;2026-08-26T16:49:07.311Z&quot;,&quot;position&quot;:9,&quot;description&quot;:&quot;Frontend application and API servers for Pages builds&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:null,&quot;id&quot;:&quot;vg70hn9s2tyj&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Copilot&quot;,&quot;created_at&quot;:&quot;2022-06-21T16:04:33.017Z&quot;,&quot;updated_at&quot;:&quot;2026-08-17T21:15:46.595Z&quot;,&quot;position&quot;:10,&quot;description&quot;:null,&quot;showcase&quot;:true,&quot;start_date&quot;:&quot;2022-06-21T00:00:00.000Z&quot;,&quot;id&quot;:&quot;pjmpxvq2cmr2&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Codespaces&quot;,&quot;created_at&quot;:&quot;2021-08-11T16:02:09.505Z&quot;,&quot;updated_at&quot;:&quot;2026-07-14T09:51:08.862Z&quot;,&quot;position&quot;:11,&quot;description&quot;:&quot;Orchestration and Compute for GitHub Codespaces&quot;,&quot;showcase&quot;:true,&quot;start_date&quot;:&quot;2021-08-11T00:00:00.000Z&quot;,&quot;id&quot;:&quot;h2ftsgbw7kmk&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false},{&quot;status&quot;:&quot;operational&quot;,&quot;name&quot;:&quot;Copilot AI Model Providers&quot;,&quot;created_at&quot;:&quot;2026-04-17T12:33:08.827Z&quot;,&quot;updated_at&quot;:&quot;2026-08-27T12:12:58.358Z&quot;,&quot;position&quot;:12,&quot;description&quot;:null,&quot;showcase&quot;:true,&quot;start_date&quot;:&quot;2026-04-17T00:00:00.000Z&quot;,&quot;id&quot;:&quot;cnnb39dkkk82&quot;,&quot;group_id&quot;:null,&quot;page_id&quot;:&quot;kctbh9vrtdwd&quot;,&quot;group&quot;:false,&quot;only_show_if_degraded&quot;:false}],&quot;months&quot;:[{&quot;name&quot;:&quot;August&quot;,&quot;year&quot;:2026,&quot;starts_on&quot;:6,&quot;days&quot;:31,&quot;incidents&quot;:[{&quot;code&quot;:&quot;5bn0vk444m1w&quot;,&quot;name&quot;:&quot;Disruption with GitHub Billing&quot;,&quot;message&quot;:&quot;This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e26\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e23:37\u003c/var\u003e - Aug \u003cvar data-var=&#39;date&#39;\u003e27\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e19:44\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;tx9qn4khd664&quot;,&quot;name&quot;:&quot;Incident with Copilot AI Model Providers&quot;,&quot;message&quot;:&quot;This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e27\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e10:04\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e12:12\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;kfspvrz14xr0&quot;,&quot;name&quot;:&quot;Incident with Actions and Pull Requests&quot;,&quot;message&quot;:&quot;This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e26\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e22:56\u003c/var\u003e - Aug \u003cvar data-var=&#39;date&#39;\u003e27\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e00:26\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;y1t7p9fzrlj2&quot;,&quot;name&quot;:&quot;Incident with Actions&quot;,&quot;message&quot;:&quot;On August 26, 2026 from 15:02 to 15:45 UTC, Actions jobs failed to start. The following 2 hours until 17:40 UTC, Actions runs were delayed starting by more than 5 minutes as the system caught up with delayed load. This impact was triggered by saturation of writes to the database primary used by the service processing triggers for Actions workflows. The primary was failed over, but the system did not fully recover. The saturation was caused by growing daily peak load combined with an upstream issue in GitHub’s event processing infrastructure, https://www.githubstatus.com/incidents/hcbtzksccj2f, which caused burst amplification of already-high load. Downstream throttles that were later used to recover were set ~10% too high to protect the system.  \u003cbr /\u003e\u003cbr /\u003eAt 15:45 UTC, throttling combined with service restarts recovered the service’s core health. Those throttles were gradually raised between 15:54 and 17:22 to restore full webhook processing for Actions runs. This ramp was deliberately slow to ensure we did not re-overwhelm the system given our original throttling was now known to be incorrectly set. The queue of webhook events was fully burned down at 17:40 UTC. \u003cbr /\u003e\u003cbr /\u003e3.7% of larger-runner jobs, along with some scale-set self-hosted jobs, remained stuck in queued or “waiting for runner” state. We deployed a change to force-revoke jobs in this state, and they transitioned to failed at 18:40 UTC, about 50 minutes after incident mitigation. Releasing these jobs also freed hosted concurrency for larger-runner jobs. \u003cbr /\u003e\u003cbr /\u003eCustomers using concurrency groups saw longer impact due to a separate issue where runners assigned to a subset of jobs disconnected before the force-revoke mitigation was deployed, which prevented runner acquisition from progressing and left jobs in a waiting-for-runner state. This was resolved at 01:00 UTC on August 27. \u003cbr /\u003e\u003cbr /\u003eSome runs triggered during the 15:02-15:45 UTC incident window encountered a bug that left them showing as queued even after service recovery. In the backend, these runs had already failed and will automatically move to canceled state 24 hours after creation. As follow-up, we are fixing the root cause of this queued state and improving our ability to bulk-cancel affected runs. \u003cbr /\u003e\u003cbr /\u003eSeveral changes to improve the general scalability of this part of Actions were already complete and deploying to production. Rollout of those changes will be complete within the next 24 hours. Further work to improve scale, resiliency, and more graceful degradation of Actions workflows are in flight. We are also taking a repair item to accelerate clearing of stuck queued or waiting jobs in similar future cases.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e26\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:11\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:01\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;hcbtzksccj2f&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e26\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:09\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e16:07\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;lyppgxbq1nyk&quot;,&quot;name&quot;:&quot;Actions delays in starting runs&quot;,&quot;message&quot;:&quot;On August 24, 2026, between 13:33 UTC and 14:04 UTC,  3.8% of Actions runs experienced start delays over 5 minutes with 1.25% of Actions runs failing outright. \u003cbr /\u003e \u003cbr /\u003eThe incident was caused by a disk failure on a node hosting one of many service instances responsible for processing runner assignment events. Typically, pods on unhealthy nodes are removed and replaced automatically without impact. In this case, although the node was severely degraded and unable to perform disk operations, it continued sending healthy signals, preventing the system from immediately moving its work elsewhere. During this period, events assigned to the affected component accumulated until an automatic rebalance redirected processing to healthy components at 13:54 UTC. The queue backlog was cleared at 14:00 UTC, and processing returned to normal by 14:04 UTC. \u003cbr /\u003e\u003cbr /\u003eTo prevent a recurrence, we are improving detection and automated remediation for unhealthy nodes that aren’t fully offline. We are also strengthening application-level resiliency, so stalled consumers are automatically removed quickly and their work reassigned without waiting for the affected node to recover.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e24\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e13:56\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e14:34\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;wt3hjqcrczfg&quot;,&quot;name&quot;:&quot;Elevated errors on Fable 5 due to upstream provider&quot;,&quot;message&quot;:&quot;On August 24th, 2026, between approximately 06:35 and 07:25 UTC, the Copilot service experienced a degradation of the Claude Fable 5 model due to an issue with our upstream provider. Users encountered elevated error rates when using Claude Fable 5, with requests sometimes failing mid-response. No other models were impacted.\u003cbr /\u003e\u003cbr /\u003eThe issue was resolved by a mitigation put in place by our provider. GitHub is working with our provider to further improve the resiliency of the service to prevent similar incidents in the future.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e24\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e07:12\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e07:58\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;wms44hv62t3p&quot;,&quot;name&quot;:&quot;Degraded Git Operations over SSH&quot;,&quot;message&quot;:&quot;On August 21, 2026, between 14:00 and 14:07 UTC, dotcom Git operations over SSH were degraded. Successful Git operations over SSH fell by more than 95% for during the peak impact window, making clone, fetch, or push over SSH effectively unavailable to most users for approximately four minutes. Git operations over HTTPS were not affected.  \n\nThe incident was caused by a software defect in our load-balancing infrastructure that was triggered by a configuration change. The defect only occurred when connections passed through multiple layers of load balancers running the new configuration, which meant it was not detected during canary testing. \n\nWe mitigated the incident by rolling back the configuration change.  \n\nWe are adding regression coverage for multi-layer load-balancer configurations and improving monitoring and alerting for Git operations over SSH to reduce our time to detection and mitigation of similar issues in the future.&quot;,&quot;impact&quot;:&quot;none&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e21\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:00\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e14:00\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;bhbcjn4n3jzp&quot;,&quot;name&quot;:&quot;Intermittent failures creating agent tasks&quot;,&quot;message&quot;:&quot;Between 13:57 UTC on August 20 and 00:37 UTC on August 21, 2026, some users of the Copilot Cloud Agent experienced delays of up to 60 to 90 minutes in seeing the status and results of their agent tasks. The agent tasks themselves continued to run and complete during this time; only the visibility of their status was delayed.\u003cbr /\u003e\u003cbr /\u003eThe cause was a regional outage in a third-party cloud database service that Copilot uses to store agent task status. We failed over the affected database to a healthy region, added processing capacity to work through the backlog, and restored normal operation once the underlying service recovered. No task data was lost during the incident.\u003cbr /\u003e\u003cbr /\u003eTo prevent repetition of similar incidents, we are removing the database configuration that made us vulnerable to this regional outage and improving our database failover procedures.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e20\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:43\u003c/var\u003e - Aug \u003cvar data-var=&#39;date&#39;\u003e21\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e00:37\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;bmpybhnrky3x&quot;,&quot;name&quot;:&quot;Intermittent failures in runner group and runner-related permissions pages&quot;,&quot;message&quot;:&quot;On August 18, 2026, between 05:02 UTC and 11:30 UTC, customers were unable to view or manage Actions Runners and Runner Groups through the GitHub UI and API. \u003cbr /\u003e\u003cbr /\u003eThe issue was caused by failures in backend requests reading runner and runner group data. The failures were caused by an expired authentication certificate unique to this service. The certificate had been rotated in KeyVault, but a step to enable use at runtime had been paused to prevent recurrence of previous incidents triggered by this operation. \u003cbr /\u003e\u003cbr /\u003eThe impact was mitigated by completing the enablement of the new certificate in the backend system. We have added additional monitoring to this and other certificates. This service is also in the process of being replaced as part of our availability and scale work, bringing this authentication path and secret management in line with patterns across all GitHub services.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e18\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e07:40\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e11:42\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;gx7js8bd0jpz&quot;,&quot;name&quot;:&quot;Incident with Actions&quot;,&quot;message&quot;:&quot;On August 18, 2026, between 05:02 UTC and 11:30 UTC, customers were unable to run jobs on Actions Larger Runners and were unable to view or manage Actions Runners and Runner Groups through the GitHub UI and API. \u003cbr /\u003e\u003cbr /\u003eThese issues were caused by failures in backend requests resolving essential metadata for starting Larger Runner workflow runs and for reading runner and runner group data. The failures were caused by an expired authentication certificate unique to this service. The certificate had been rotated in KeyVault, but a step to enable use at runtime had been paused to prevent recurrence of previous incidents that had been triggered by this operation. \u003cbr /\u003e\u003cbr /\u003eWe mitigated the issues by completing the enablement of the new certificate in the backend system. We have added additional monitoring to this and other certificates. The relevant service is also in the process of being replaced as part of our availability and scale work, bringing this authentication path and secret management in line with patterns across all GitHub services.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e18\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e09:36\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e10:23\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;zkxwbgr0cnmx&quot;,&quot;name&quot;:&quot;Incident with GitHub.com&quot;,&quot;message&quot;:&quot;On August 17, 2026, from 13:28–21:15 UTC (7h 47m), GitHub.com experienced elevated errors and latency across Issues, Pull Requests, APIs, Actions, and Copilot. At peak, web/API error rates were approximately 20%, while archive and raw-content downloads reached approximately 50%. SAML/OIDC authentication, SCIM, and Team Sync were also affected, as well as Actions workflows in GHEC with Data Residency that depend on public workflow step definitions hosted on GitHub.com. Most services recovered by 16:36 UTC as our Central US datacenter recovered; Actions was degraded until approximately 18:03 UTC; and Copilot Token Service fully recovered by 21:02. \u003cbr /\u003e\u003cbr /\u003eSome of the failing traffic was moved from Central US to Northern Virginia where it was served successfully until the network failure in Central US was debugged and resolved. Delayed replies to a single internal endpoint triggered a latent retry bug in VS Code that amplified traffic by approximately 10x and caused delayed recovery for the Copilot Token Service. \u003cbr /\u003e\u003cbr /\u003eThe immediate cause of the failure was network saturation on load balancers in Central US due to a new peak in traffic. Originally this was caused by an Istio sidecar pod reaching its concurrency limits and failing to auto scale correctly because of a misconfigured policy that watched host service but not sidecar limits. One failure cascaded to more and eventually four HAProxy nodes exhausted their flow limits, degrading the gateway auth path and causing widespread authentication latency and failures. The problem was worsened by optimistic retry logic which overloaded internal load balancers. Pausing HAProxy on those nodes simultaneously produced immediate broad recovery. \u003cbr /\u003e\u003cbr /\u003eThe retry storm in Northern VA was fixed by 1) temporarily reducing gateway retry logic with a PR and 2) blocking inbound Copilot Token Service token requests at the load balancers with a 403, and then gradually ramping back up traffic per-site to allow callers to succeed. \u003cbr /\u003e\u003cbr /\u003eResidual Copilot authentication failures continued because client retry behavior amplified load: a failed token operation could generate many extra requests and enter a retry loop. Copilot Token Service traffic increased from a normal 7–9K RPS to 70–100K RPS. Reducing gateway authentication retries and blocking retry-triggering responses stabilized Copilot Token Service and completed recovery. \u003cbr /\u003e\u003cbr /\u003eComplicating factors that impeded recovery included a number of scraping attacks on codeload endpoints. \u003cbr /\u003e\u003cbr /\u003eTo prevent recurrence, our follow-up actions include: \u003cbr /\u003e\u003cbr /\u003e- Correcting autoscaling policies to account for service-mesh sidecar concurrency and capacity. \u003cbr /\u003e\u003cbr /\u003e- Auditing Istio request, concurrency, and scaling limits across affected services. \u003cbr /\u003e\u003cbr /\u003e- Reviewing retry limits and backoff behavior across gateways and clients. \u003cbr /\u003e\u003cbr /\u003e- Addressing the VS Code retry behavior that amplified Copilot token traffic. \u003cbr /\u003e\u003cbr /\u003e- Improving load-balancer capacity monitoring and regional failover safeguards.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e17\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e13:40\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e21:15\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;pf25whpq58hh&quot;,&quot;name&quot;:&quot;Disruption with GHEC Team Sync&quot;,&quot;message&quot;:&quot;On August 13, 2026, from 15:31:21 UTC to 18:27:55 UTC, GitHub Enterprise Cloud team synchronization was degraded for enterprises using personal accounts. Organization teams experienced delays of up to 3 to 13 hours (median 8 hours) when syncing with IdP groups, resulting in delayed access grants or removals for enterprise users across 2.8% of teams. \u003cbr /\u003e\u003cbr /\u003eA temporary change introduced to address a previous issue due to increased usage of this feature remained active after it was intended to be removed, causing synchronization delays during periods of high volume. We removed the temporary change and provisioned additional resources to handle the increased volume.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e13\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e16:21\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:27\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;24t8gsgqx2qb&quot;,&quot;name&quot;:&quot;Errors with the Fable 5 Model in Copilot&quot;,&quot;message&quot;:&quot;On August 13th, 2026, between approximately 14:06 and 15:47 UTC, the Copilot service experienced a degradation of the Claude Fable 5 model due to an issue with our upstream provider. Users encountered elevated error rates, peaking at 43% and averaging 12%. Users who selected Auto or alternative models were unaffected.\u003cbr /\u003e\u003cbr /\u003eThe issue was resolved by a mitigation put in place by our provider. GitHub is working with our provider to further improve the resiliency of the service to prevent similar incidents in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e13\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:43\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e15:47\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;k8vbzwqjkxzn&quot;,&quot;name&quot;:&quot;Incident with Webhooks&quot;,&quot;message&quot;:&quot;This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e13\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:45\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e15:36\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;lsvy8xsf0gxv&quot;,&quot;name&quot;:&quot;Disruption with Login and Release Asset downloads&quot;,&quot;message&quot;:&quot;On August 12 and 13, 2026, some anonymous (logged-out) requests to github.com experienced HTTP 5xx errors when loading pages like the sign-in page, and when downloading release assets, due to an unusual traffic pattern that repeatedly overloaded a part of our infrastructure that serves these types of requests. There were three windows of impact: (1) August 12 from 16:34 to 18:34 UTC, with an average error rate of 16.16% that peaked at 28.6%; (2) August 12 from 19:00 to 22:56 UTC, with an average error rate of 16.55% that peaked at 24.18%; and (3) August 13 from 06:19 to 08:05 UTC, with an average error rate of 2.01% that peaked at 7.49%.\u003cbr /\u003eRequests from signed-in users were unaffected.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incidents by applying traffic controls at our network edge that limited any requests matching the pattern identified previously, thereby preventing overload on our systems.\u003cbr /\u003e\u003cbr /\u003eSince these incidents occurred, we have tightened our monitoring systems to alert server-side errors that affect logged-out traffic. We are also working to further strengthen our edge protections and reduce the time to detect and mitigate similar incidents.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e12\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e21:39\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e22:56\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;76t89hbfb09h&quot;,&quot;name&quot;:&quot;Incident with Pull Requests and Issues&quot;,&quot;message&quot;:&quot;Between 16:03 and 16:29 UTC on August 12, some users encountered errors when viewing pull requests, issues, and search results. During this period, about 1.9% of Pull Request requests and 0.9% of Issues requests failed. During a database migration, two indexes were removed while application settings still referenced them, causing affected requests to fail. We detected the issue after the migration reached one database shard and before it progressed to the remaining shards. We restored service by disabling both settings. We are improving safeguards around database migrations and application configuration to prevent similar mismatches from causing errors.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e12\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e16:16\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e16:41\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;vm1w8zq95wkt&quot;,&quot;name&quot;:&quot;Incident with GraphQL API Requests&quot;,&quot;message&quot;:&quot;On August 11, 2026, between 14:00 UTC and 16:00 UTC the GraphQL API service was degraded and customers in  saw higher than normal timeouts. On average, the timeout rate was 0.06% and peaked at 0.14% of requests routing to the service. \u003cbr /\u003e\u003cbr /\u003eThis was due to increased utilization at one of our sites which caused resource contention across our dependencies, leading to an increase in timeouts for GraphQL requests. We mitigated the incident by increasing capacity to alleviate the capacity bottleneck.  \u003cbr /\u003e\u003cbr /\u003eWe are working to improve our monitoring so that we can proactively reduce the impact of high consumption requests in addition to scaling up; Additionally, we will improve our time to detection and mitigation of issues like this one in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e11\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:50\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e20:06\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;1t7x65n7kvt1&quot;,&quot;name&quot;:&quot;Disruption with Copilot for access to some models&quot;,&quot;message&quot;:&quot;On August 10, 2026, between 19:48 UTC and 20:49 UTC, GitHub Copilot users saw an incomplete list of available models. During this window, the service could return as few as one model instead of the full catalog. Requests that tried to use a model missing from that shortened list failed with a \&quot;model not found\&quot; error. Copilot requests that used an available model were not affected. This did not affect customers on data-residency (Proxima) environments.\u003cbr /\u003e\u003cbr /\u003eThe issue was caused by a change to how model data was published, which our systems could not read back correctly and fell back to a limited default list.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by 20:49 UTC and deployed a fix to prevent immediate recurrence by 21:50 UTC. We are adding validation and retry safeguards so that model data is verified before it is served.\u003cbr /\u003e\u003cbr /\u003eWe apologize for the disruption.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e10\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e20:27\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e21:50\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;s19bth7wzkf7&quot;,&quot;name&quot;:&quot;Disruption with creation of fine grained personal access tokens&quot;,&quot;message&quot;:&quot;On August 10, 2026, between 17:16 and 18:21 UTC, users were unable to create new fine-grained personal access tokens (FG PAT) through the GitHub website. When a user submitted the FG PAT creation form, they were returned to the FG PAT list without an error message and no FG PAT was created. Creating classic personal access tokens, as well as editing or deleting existing FG PAT were not affected.\u003cbr /\u003e\u003cbr /\u003eThe cause was a change to how the website loads certain front-end JavaScript that was enabled for all users at 17:15 UTC; the change interacted with an issue in the token creation form&#39;s confirmation step that prevented it from running, so the final submission that actually creates the token never completed. Because the page still loaded and the server returned a normal response, the failure produced no error message. GitHub mitigated the incident by disabling the change at 18:21 UTC, at which point token creation recovered immediately, and the incident was resolved at 18:46 UTC.\u003cbr /\u003e\u003cbr /\u003eTo reduce the chance of recurrence, GitHub is adding monitoring and alerting for anomalies in the FG PAT creation success rate and is removing the issue in the FG PAT creation form that prevented the confirmation step from running. GitHub is also adding automated detection of the issue so other areas of the GitHub front end do not repeat the problem.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e10\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e18:02\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:46\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;qcvjkzcs7j74&quot;,&quot;name&quot;:&quot;Incident with Actions&quot;,&quot;message&quot;:&quot;On August 6, 2026, between 15:05 UTC and 00:14 UTC on August 7, GitHub Actions experienced degraded availability. During the incident, workflow runs failed or remained queued for an extended period of time. Customers using both GitHub-hosted and self-hosted runners were affected. At peak, 71% of workflow runs experienced infrastructure failures and 75% of the remaining workflow runs were delayed by more than 5 minutes. \u003cbr /\u003e\u003cbr /\u003eThe incident was triggered by a routine deployment to an internal Actions service responsible for processing events and generating Actions jobs. The deployment exposed an existing capacity and concurrency weakness. As pods were replaced during the deployment, remaining capacity became saturated, causing services to crash and triggering a cascading impact across multiple clusters and downstream services. \u003cbr /\u003e\u003cbr /\u003eThese services recovered at 17:00 after expanding capacity, throttling incoming webhook-triggered work to allow the system to recover, and increasing processing capacity for the backlog of affected events. \u003cbr /\u003e\u003cbr /\u003eAs the incident progressed, a backlog of work accumulated across the systems responsible for assigning jobs to runners. Due to a latent bug in one of the services responsible for job assignment, runners were getting assigned jobs that were no longer valid and then getting stuck retrying those jobs, preventing them from picking up valid work. \u003cbr /\u003e\u003cbr /\u003eThis second stage of impact was mitigated by deploying changes to prevent runners from repeatedly attempting to acquire invalid jobs. These mitigations allowed the accumulated queues to drain and Actions to recover to normal operation. \u003cbr /\u003e\u003cbr /\u003eSome Actions Runner Controller (ARC) runners remained stuck after the incident. A mitigation deployed during the incident inadvertently affected these runners, causing some to remain offline until they were manually recovered. We subsequently rolled back the change and are adding automatic recovery in upcoming Runner and ARC releases. \u003cbr /\u003e\u003cbr /\u003eSome jobs created during the incident were also left stuck unable to be retried or canceled.  CLI and UI solutions for customers to address these were shared at https://github.com/orgs/community/discussions/204152#discussioncomment-17946043. \u003cbr /\u003e\u003cbr /\u003eTo prevent recurrence, we are making improvements to deployment and capacity safeguards for the affected services, strengthening monitoring for the conditions that preceded the incident, improving the resiliency and recovery of queued work and runner assignment, and adding automatic recovery for self-hosted runners affected by similar failure conditions. We are also making additional improvements to reduce the risk of cascading failures and accelerate recovery during large-scale Actions disruptions.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e6\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:22\u003c/var\u003e - Aug \u003cvar data-var=&#39;date&#39;\u003e7\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e02:04\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;1xqvzyv99skw&quot;,&quot;name&quot;:&quot;Incident with Pages - Deployment Lag&quot;,&quot;message&quot;:&quot;On August 6, 2026, at 07:00 UTC, a configuration change inadvertently reduced the capacity of the service that processes GitHub Pages deployments. As traffic increased over the following hours, latency in the deployment pipeline progressively increased. \u003cbr /\u003e\u003cbr /\u003eAt 12:09 UTC, latency crossed the alerting threshold and the team began investigating. We reverted the invalid configuration and applied additional mitigations, including reducing status deployment processing to lower the load on our Redis cluster. Latency returned to normal levels at 15:40 UTC. \u003cbr /\u003e\u003cbr /\u003eCustomer impact occurred from 11:34 to 15:32 UTC. During this period, we failed to process approximately 128,000 deployments. \u003cbr /\u003e\u003cbr /\u003eWe have updated our alerts to detect elevated processing latency sooner and to notify us immediately when latency causes deployment processing failures. We&#39;ve confirmed this incident was not fully captured by our availability metrics. In the coming days, we&#39;ll update how GitHub Pages availability is measured so incidents like this are accurately reflected going forward.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e6\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:03\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e16:22\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;9wzhl5jr80jt&quot;,&quot;name&quot;:&quot;Some Copilot Cloud Agent jobs not starting&quot;,&quot;message&quot;:&quot;On August 5, 2026, between 11:02 and 11:54 UTC, the GitHub Copilot cloud agent service was degraded and new cloud agent jobs were delayed from starting. During this period 100% of newly submitted agent jobs were affected. The incident was limited to delay of cloud agent jobs. No jobs were lost and the queued backlog was processed by 13:00 UTC. This was due to an internal rate limit used to protect service availability that was enabled more broadly than intended delaying more traffic than expected. \u003cbr /\u003e \u003cbr /\u003eThe service recovered when the rate limit window expired. We then tuned the control so it no longer affected unrelated coding agent traffic. \u003cbr /\u003e \u003cbr /\u003eWe are working to improve the control&#39;s scoping and our monitoring and alerting to reduce our time to detection and mitigation of similar issues in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e5\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e11:38\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e13:00\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;7s119p1yxttr&quot;,&quot;name&quot;:&quot;Incident with Copilot&quot;,&quot;message&quot;:&quot;On 2026-08-03, between 06:52 and 11:25 UTC, some GitHub Copilot users experienced errors when using chat and agent features. Requests to list the available models failed, and because every chat or agent interaction begins by retrieving the list of models, affected users saw their requests fail. On average about 3% of these model-listing requests failed during the incident (roughly 97% succeeded), but failures were significantly higher during peak-traffic periods, at times approaching 100% for the affected internal lookups. Approximately 4,066 users were affected in a single 60-minute window, concentrated among IDE-based clients. The underlying AI models themselves remained healthy throughout.\u003cbr /\u003e\u003cbr /\u003eThe incident was caused by an increase in how often clients requested the model list, which pushed an internal user-authorization lookup past a rate limit; the rate-limited responses were surfaced to users as errors. We mitigated the impact by increasing how long Copilot caches that authorization lookup, which reduced load on the internal service, and we have additional capacity and rate-limit changes in progress. To prevent recurrence we are improving monitoring for this class of failure, adjusting cache and rate-limit settings, and coordinating with client teams on request patterns.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e3\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e09:53\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e11:25\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;sj1tzyrx599x&quot;,&quot;name&quot;:&quot;Incident with Copilot AI Model Providers&quot;,&quot;message&quot;:&quot;On August 1, 2026, between 17:47 UTC and 18:20 UTC, users of the Fable 5 model in GitHub Copilot experienced increased request failures and latency. The average failure rate across all Copilot requests was 0.007%, while failures for Fable 5 peaked at 5.6%. Other models remained available. This was caused by degradation of an upstream model provider.\u003cbr /\u003e\u003cbr /\u003eThe affected endpoint recovered, and we monitored the service until error rates and latency returned to normal levels. We are working to add endpoint redundancy to mitigate similar provider issues in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e1\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e18:03\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:44\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;kk183dslzdzd&quot;,&quot;name&quot;:&quot;Degraded availability GPT 5.6 Luna&quot;,&quot;message&quot;:&quot;On August 1st, 2026, the GPT-5.6 Luna model in GitHub Copilot experienced degraded availability in intermittent time intervals between ~08:05 UTC and ~16:30 UTC. Specifically the timeframes observed were 10:00-10:20 UTC, 10:45-11:50 UTC, 13:00-14:25 UTC, and 16:00-16:30 UTC. During this time, requests to GPT-5.6 Luna in Copilot chat and IDE surfaces frequently failed or timed out. This was caused by an issue with an upstream model provider. Other Copilot models were not affected, and users could continue working by selecting another model or &#39;Auto&#39;. Availability for GPT-5.6 Luna fully recovered once the provider resolved their outage at 16:30 UTC.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Aug \u003cvar data-var=&#39;date&#39;\u003e1\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e11:16\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e12:30\u003c/var\u003e UTC&quot;}]},{&quot;name&quot;:&quot;July&quot;,&quot;year&quot;:2026,&quot;starts_on&quot;:3,&quot;days&quot;:31,&quot;incidents&quot;:[{&quot;code&quot;:&quot;9tpgqq1h4bs7&quot;,&quot;name&quot;:&quot;Copilot model Claude Fable 5 experiencing elevated errors&quot;,&quot;message&quot;:&quot;On July 30, 2026, the Claude Fable 5 model in GitHub Copilot experienced degraded availability for approximately 73 minutes, from 08:33 to 09:46 UTC. During this time, requests to Claude Fable 5 in Copilot chat and IDE surfaces frequently failed or timed out. This was caused by an issue with an upstream model provider. Other Copilot models were not affected, and users could continue working by selecting another model or &#39;Auto&#39;. Availability for Claude Fable 5 fully recovered once the provider resolved their outage at 09:46 UTC, and we confirmed resolution at 10:12 UTC.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e30\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e09:07\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e10:12\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;dsrfymph7my0&quot;,&quot;name&quot;:&quot;Incident with Copilot AI Model Providers&quot;,&quot;message&quot;:&quot;On July 29, 2026, between 19:45 UTC and 21:51 UTC, users of the Fable 5 model in GitHub Copilot experienced increased request failures and latency. The average failure rate across all Copilot requests was 0.006%, while failures for Fable 5 peaked at 21%. Other models remained available. This was caused by degradation of an upstream model provider.\u003cbr /\u003e\u003cbr /\u003eThe affected endpoint recovered, and we monitored the service until error rates and latency returned to normal levels. We are working to add endpoint redundancy to mitigate similar provider issues in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e29\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e20:07\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e21:51\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;75g5xmzptjqb&quot;,&quot;name&quot;:&quot;Incident with Actions&quot;,&quot;message&quot;:&quot;On July 29, 2026, from 14:51 UTC to 15:28 UTC, GitHub Actions experienced elevated REST API request timeouts and errors, failures registering runners, and delayed workflow run starts for customers whose traffic was served by a single infrastructure site. This was caused by an under-provisioned internal Actions service in that site: under increased load its instances ran out of memory and became unresponsive, and because Actions API requests wait synchronously on that service, requests routed through the affected site stalled and timed out. During the incident, approximately 2% of workflows were delayed. Requests served by other sites remained unaffected. Both standard and larger hosted runners routed through the affected site could see delayed job starts. \u003cbr /\u003e\u003cbr /\u003eThe issue was mitigated by scaling out the runner-administration service in the affected site and increasing the replica count, which restored API availability and returned workflow run starts to normal. We are working to add horizontal autoscaling, memory-saturation alerting, and scaling-forecast monitoring for this service, along with responder playbooks, to reduce the likelihood of similar issues in the future.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e29\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:26\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e16:00\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;fmmsrcg5x638&quot;,&quot;name&quot;:&quot;Incident with GraphQL API Requests&quot;,&quot;message&quot;:&quot;On July 26, 2026 at 21:34 UTC we began seeing intermittent errors on the GitHub GraphQL API. A subset of GraphQL API requests returned HTTP 502 errors in short bursts. During the impact window an average of 0.09% of GraphQL API requests in the affected region failed, with a peak of 0.50% of requests failing during the worst two-minute period at 03:02 UTC on July 27. Requests that failed generally succeeded when retried, and no data was lost or altered. Other GitHub services were not affected.\u003cbr /\u003e\u003cbr /\u003eThe errors were traced to a single group of servers handling a share of GraphQL API traffic. Application processes on that group intermittently closed connections before completing responses. Impact ended at 03:52 UTC on July 27 when those processes were replaced, and we resolved the incident at 04:09 UTC on July 27 after confirming error rates had returned to normal.\u003cbr /\u003e\u003cbr /\u003eWe are still investigating why those processes closed connections, and that work is being carried out by the team that owns the underlying compute platform. In the meantime we are adding detection and automated mitigation for when a single group of servers behaves differently from its peers.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e27\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e03:53\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e04:09\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;pz7g535gbs6p&quot;,&quot;name&quot;:&quot;Actions run failures and delays&quot;,&quot;message&quot;:&quot;Please refer to the combined summary in this related incident: https://www.githubstatus.com/incidents/s65j9gslmfm8&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e25\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e12:31\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e13:13\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;vv9vvksmj4s9&quot;,&quot;name&quot;:&quot;Several GPT models degraded&quot;,&quot;message&quot;:&quot;On July 25, 2026, between 09:07 and 10:04 UTC, the GPT-5.2, GPT-5.3-Codex, GPT-5.4, GPT-5.4 Mini, GPT-5.6 Sol, GPT-5.6 Terra and GPT-5.6 Luna models experienced degraded availability in GitHub Copilot products and IDE surfaces. Requests to these models had an average failure rate of 5.6%. Other Copilot models remained available as alternatives.\u003cbr /\u003e\u003cbr /\u003eThe degradation was caused by an issue with an upstream model provider. Success rates returned to normal after the upstream issue was mitigated, and we continued monitoring before resolving the incident. We are working on improving the automated failover for the affected models to prevent similar incidents in the future.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e25\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e09:42\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e10:11\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;s65j9gslmfm8&quot;,&quot;name&quot;:&quot;Incident with Actions&quot;,&quot;message&quot;:&quot;On July 25, 2026, GitHub Actions experienced two related periods of degradation that caused some workflow runs to be delayed by more than 5 minutes or end with infrastructure failures. \u003cbr /\u003e\u003cbr /\u003eFirst period (08:45 – 09:13 UTC): During planned maintenance on a critical-path Redis cluster for Actions, one participating region was left in a degraded state. Separately, an independent capacity operation temporarily removed another region from the cluster and redirected its traffic to the degraded region. This created cross-region inconsistencies in job-assignment state, causing workflow runs to be delayed, exhaust retries, or fail outright. At peak, about 7% of runs were delayed by more than 5 minutes, and 25% of runs failed with an infrastructure error during the course of the incident. We mitigated the incident at 09:13 UTC by returning traffic to its normal distribution. \u003cbr /\u003e\u003cbr /\u003eSecond period (12:08 – 12:48 UTC): As part of mitigating the first incident, traffic was returned to the regional instance that was still undergoing its capacity increase. Multiple Redis nodes in the scaling region experienced failures, increasing traffic to healthy nodes and causing connection limits to be reached on many nodes. At peak, 30% of runs were delayed by more than 5 minutes, and 60% of runs failed with an infrastructure error during the course of the incident. We mitigated the incident at 12:48 UTC by redirecting workflow traffic away from the scaling region. \u003cbr /\u003e\u003cbr /\u003eWe are adding stronger regional health and capacity checks before maintenance and requiring a stable observation period before restoring traffic. We are also improving automated connection resiliency, and partnering with our platform dependency to automatically detect and remediate unhealthy cluster members and shard imbalance.  More generally, we already had work underway to improve the resiliency and scale of this piece of Actions infrastructure.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e25\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e08:59\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e09:25\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;jxd617hfwfq8&quot;,&quot;name&quot;:&quot;Incident with Pull Requests&quot;,&quot;message&quot;:&quot;Between July 24, 19:17 UTC and July 24, 20:02 UTC, users were unable to create pull requests due to a database schema change. In total, 113,930 pull request creation attempts were impacted across 50,904 users, with an average error rate of 1.75% and a maximum error rate of 2.25% for all requests to Pull Requests service. Existing pull requests and other GitHub functionality were not affected. The issue was resolved by reverting the change to the affected database, upon which pull request creation immediately resumed.\u003cbr /\u003e\u003cbr /\u003eThe root cause was related to a backfill workflow into the Vitess keyspace hosting Pull Request data. The backfill Vitess command encountered errors and increased VReplication lag, and the workflow was canceled at 19:17 UTC. The cancellation executed a misunderstood Vitess codepath that dropped the backing table to the target keyspace, leaving a non-existent reference that resulted in errors creating Pull Requests. The mitigation was executing a command to drop the vschema reference to the dropped table, allowing Pull Request creation to resume.\u003cbr /\u003e\u003cbr /\u003eWe are adding stronger pre-flight validation to our tooling to prevent similar issues and expanding lower-environment support to provide better test coverage end-to-end before promoting them to production. We&#39;re also fixing our backfill migration tooling to protect from this specific codepath.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e24\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e19:37\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e20:23\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;yjysg0xrl67m&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;On July 24th at 16:04 UTC, a loss of connectivity occurred in network paths in one of our three physical data center availability zones (AZs). This resulted in packet loss due to the remaining active paths becoming saturated. Our data centers use a leaf-spine switch fabric in each compute cage, and an aggregation layer interconnecting the spines from each cage within each AZ. The loss of connectivity affected links between one cage’s spine switches and the aggregation layer within that specific AZ. \u003cbr /\u003e\u003cbr /\u003eWorkloads depending on compute resources in this cage became degraded due to packet loss, and exhibited intermittent errors: \u003cbr /\u003e\u003cbr /\u003e- Actions saw 10% of jobs fail during the impact window, and 5% of jobs succeeded but with delayed starts. \u003cbr /\u003e- 27% of GitHub issues interactions saw slow requests or timeouts. \u003cbr /\u003e- 4% of GitHub Copilot requests experienced errors, though most automatically retry. \u003cbr /\u003e- 4% of git push operations saw impacts during the affected window. \u003cbr /\u003e- Authentication requests saw increased latency during the affected window, but error rates, while elevated, were \u0026lt; 1% in all cases.  \u003cbr /\u003e\u003cbr /\u003eWe were able to mitigate the outage by re-routing affected connections to available fiber paths that were allocated for future capacity upgrades. Sufficient network capacity to eliminate packet loss was restored at 17:07, with most services showing full recovery by 17:16. All paths were restored and services healthy at 17:36. \u003cbr /\u003e\u003cbr /\u003eThis incident affected 25% of available network interconnect capacity. Older cages utilize a 100Gbps network interface standard. To remove risk of reoccurrence, a planned upgrade to 400Gbps interfaces is being accelerated as much as possible, ensuring increased bandwidth available at all layers of the switch fabric for resiliency to path or device loss.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e24\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e16:17\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e17:36\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;594m87r8sw13&quot;,&quot;name&quot;:&quot;Incident With Blocked GitHub.com Traffic&quot;,&quot;message&quot;:&quot;Between July 23, 2026 at 18:45 UTC and July 24, 2026 at 11:19 UTC, an abuse mitigation update caused some legitimate customers whose traffic was routed through our Central Europe and South America edge locations to be incorrectly blocked from GitHub.com. We estimate that approximately 0.25% of GitHub.com requests were affected during this period.\n\nThis was caused by an abuse mitigation configuration that incorrectly classified legitimate traffic. We mitigated the incident by reverting the update. We are adding validation and safeguards to prevent similar incorrect blocking in the future.&quot;,&quot;impact&quot;:&quot;none&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e24\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e11:00\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e11:00\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;zq3c1jst2vkq&quot;,&quot;name&quot;:&quot;Latency issues across a number of services&quot;,&quot;message&quot;:&quot;On July 23, 2026, between 07:08 and 09:39 UTC, several services experienced delays: 8% of actions workflow runs experienced an average run start delay of 10 minutes, 5% of webhook deliveries exceeded SLO, and code scanning, repos, notifications, issues and pull requests experienced increased latency over the life of the incident.    \u003cbr /\u003e\u003cbr /\u003eThe root cause of the incident was a node of our background job processing system which did not recover after entering scheduled host maintenance.  The incident was mitigated by identifying the problematic shard and restoring its correct state, after which queue backlogs drained and services recovered.  \u003cbr /\u003e\u003cbr /\u003eTo speed mitigation, we have added monitors for nodes in this unhealthy state after maintenance operations.  To prevent future recurrence, we are adapting our lifecycle automation to verify host rejoin after a scheduled reboot.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e23\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e07:53\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e09:39\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;20frdtvv3yg6&quot;,&quot;name&quot;:&quot;Disruption with actions hosted runners&quot;,&quot;message&quot;:&quot;On July 22, 2026, between 19:36 UTC and 22:04 UTC, GitHub Actions experienced delayed and failed job starts on GitHub-hosted runners. The incident was caused by an unhealthy state in a backend data service responsible for provisioning hosted runners, preventing runner acquisition for a subset of workloads. During most of the incident, approximately 15% of workflow runs on hosted runners were delayed by more than 5 minutes, while roughly 1% failed to start.\u003cbr /\u003e\u003cbr /\u003eAt 21:49 UTC, we restored the health of the backend data replication system, allowing provisioning to recover and the accumulated workflow backlog to drain. Service performance then returned to expected levels. We are improving provisioning-service resiliency, workload distribution, and capacity balancing to reduce the likelihood and impact of similar incidents.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e22\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e20:43\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e22:09\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;g40zcbvchny4&quot;,&quot;name&quot;:&quot;Some SSH connections using deploy keys are failing&quot;,&quot;message&quot;:&quot;On July 21, 2026, between 07:41 UTC and 11:57 UTC, the SSH Authentication service was degraded and some SSH connections failed to authenticate. On average, 12.2% of SSH authentication requests failed, peaking at 15.7%. Both user RSA keys and deploy keys were impacted. This was due to a change in how our SSH service handled one public-key authentication method that caused the affected authentication attempts to be rejected as invalid. \u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by reverting the change, after which SSH authentication returned to normal. \u003cbr /\u003e\u003cbr /\u003eWe are working to expand our automated test coverage for our SSH public-key authentication flows to catch more edge cases and to improve observability and alerting on SSH authentication failures, to reduce our time to detection and mitigation of issues like this one in the future.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e21\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e10:31\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e11:57\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;fd7j2mw8xw94&quot;,&quot;name&quot;:&quot;Disruption with GPT 5.3 Codex&quot;,&quot;message&quot;:&quot;Between 06:39 and 18:11 UTC on July 20, 2026, the Copilot service experienced a degradation of the GPT 5.3 model due to an issue with our upstream provider. The upstream model provider returned intermittent errors for GPT 5.3 Codex requests, which caused some responses to fail. Auto mode requests that had selected GPT 5.3 Codex were also impacted. On average about 2% of GPT 5.3 Codex requests failed during this window. Copilot automatically routed eligible traffic away from the impacted provider to reduce customer impact. No other models were impacted.\u003cbr /\u003e\u003cbr /\u003eWe worked with the upstream provider throughout the incident and confirmed sustained recovery before resolving.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e20\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e16:03\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:37\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;8vfyvq16hzh9&quot;,&quot;name&quot;:&quot;Incident with GitHub Actions&quot;,&quot;message&quot;:&quot;Between July 19, 2026, at 23:05 UTC and July 20, 2026, at 03:55 UTC, Actions self-hosted and larger runners were unable to connect to GitHub. During this period, Actions jobs were delayed or failed when trying to acquire a runner. Jobs using standard and Mac hosted runners were not affected. Reconnection traffic from affected runners also increased load on GitHub APIs, resulting in 3-4 seconds of additional average request latency and elevated 5xx error rates. \u003cbr /\u003e\u003cbr /\u003eThe incident was caused by a certificate lifecycle management failure in a subset of internal services, resulting in an SSL certificate expiration that disrupted runner connectivity. We restored service by rotating the affected certificate. Recovery began at 02:45 UTC. By 03:55 UTC, queued workflow backlog had been processed and workflow delay rates returned to normal.\u003cbr /\u003e\u003cbr /\u003eTo prevent recurrence, we are strengthening certificate renewal automation, adding fallback expiry monitoring and alerting, and improving circuit-breaker protections during runner API disruptions to reduce the risk of cascading impact to other APIs.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e19\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e23:34\u003c/var\u003e - Jul \u003cvar data-var=&#39;date&#39;\u003e20\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e04:44\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;ph5nns5y4gxj&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;Between July 19, 2026, at 23:05 UTC and July 20, 2026, at 03:55 UTC, Actions self-hosted and larger runners were unable to connect to GitHub. During this period, Actions jobs were delayed or failed when trying to acquire a runner. Jobs using standard and Mac hosted runners were not affected. Reconnection traffic from affected runners also increased load on GitHub APIs, resulting in 3-4 seconds of additional average request latency and elevated 5xx error rates.\u003cbr /\u003e\u003cbr /\u003eThe incident was caused by a certificate lifecycle management failure in a subset of internal services, resulting in an SSL certificate expiration that disrupted runner connectivity. We restored service by rotating the affected certificate. Recovery began at 02:45 UTC. By 03:55 UTC, queued workflow backlog had been processed and workflow delay rates returned to normal.\u003cbr /\u003e\u003cbr /\u003eTo prevent recurrence, we are strengthening certificate renewal automation, adding fallback expiry monitoring and alerting, and improving circuit-breaker protections during runner API disruptions to reduce the risk of cascading impact to other APIs.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e20\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e00:25\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e01:46\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;gxycch3076xk&quot;,&quot;name&quot;:&quot;Degraded REST API Availability&quot;,&quot;message&quot;:&quot;From 22:21 UTC - 23:50 UTC on July 16, 2026, the REST API experienced significant degradation.  During this period, about 39% of REST API requests failed with HTTP 500 level responses, with the errors peaking at 44.3%. \u003cbr /\u003e\u003cbr /\u003eWe identified the issue as an infrastructure change that wrongly marked the majority of API backends in a single region as unhealthy.  As a result, requests routed to those backends failed before reaching the application layer.  \u003cbr /\u003e\u003cbr /\u003eTo prevent this from happening again, we&#39;re improving our systems to catch this kind of invalid configuration before it reaches production. We&#39;ll also audit the related systems to make them more resilient to future changes, and we&#39;re increasing our monitoring sensitivity so we&#39;re alerted to problems like this sooner.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e16\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e22:51\u003c/var\u003e - Jul \u003cvar data-var=&#39;date&#39;\u003e17\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e00:14\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;0f6hndclsk21&quot;,&quot;name&quot;:&quot;Claude Fable 5 experiencing degraded performance&quot;,&quot;message&quot;:&quot;On July 16, 2026, GitHub Copilot users experienced elevated errors when using Claude Fable 5 from 17:33 UTC until mitigation at 22:04 UTC. The average error rate was 1.4%, with a maximum error rate of 30.85%. The issue was caused by degradation at an upstream model provider; other Copilot models were not significantly affected, and users could avoid the impact by selecting another model or Auto. Service recovered after the provider mitigated the degradation.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e16\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e21:05\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e22:04\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;d35pngcy6sb9&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;On July 16, 2026, between 08:50 UTC and 09:50 UTC, the GitHub MCP Server’s web_search tool experienced elevated failures. The average error rate was 42% and peaked at 82% of requests to the tool. Other GitHub MCP Server tools were unaffected. This was caused by degradation at a downstream web search provider.\u003cbr /\u003e\u003cbr /\u003eThe incident was mitigated when the downstream provider recovered, after which we confirmed that the tool’s success rate had returned to normal.\u003cbr /\u003e\u003cbr /\u003eWe are improving the tool’s resilience and failure handling to reduce the customer impact and duration of similar incidents.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e16\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e09:13\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e12:20\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;ydpk76bj34z8&quot;,&quot;name&quot;:&quot;Incident with Webhooks&quot;,&quot;message&quot;:&quot;On July 14, 2026, between 15:17 and 15:37 UTC, a rollout to GitHub&#39;s internal webhook delivery pipeline caused a subset of webhook delivery records to not be written to our webhook deliveries store after being processed and delivered successfully. Affected deliveries would be missing from the webhook delivery UI and API and won’t be available for redelivery.\n\nThe root cause was an uncoordinated rollout: a change to how delivery records are handed off between pipeline components was deployed before the upstream components producing those records were updated to match. While the rollout was in progress, affected records were silently skipped rather than persisted, with no automatic retry. The impact ended as soon as the rollout was completed.\n\nAbout 2.4M delivery records were skipped (approximately 4% of the 20-minute impact window, 0.04% of a typical 24-hour period). Importantly, 95% of these skipped deliveries reached customer endpoints successfully, only the record of the delivery is missing. Of the ~5% that failed to reach customer endpoints, only ~1.4% (5,463) map to webhooks that retried their deliveries in the past 28 days.\n\nTo prevent recurrence, we are improving our automated detection of unsafe schema changes and tightening rollout coordination for changes that span multiple components in the pipeline.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e14\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e17:38\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:01\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;dfpfsngcwywf&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;On July 14, 2026, the GitHub Codespaces service was degraded during two periods — between 06:00 UTC and 09:56 UTC, and again between 10:54 UTC and 12:53 UTC — and some users experienced intermittent failures or delays when creating new codespaces. Impact was concentrated in a subset of geographic regions. During the first period, the error rate averaged 0.5% and peaked at 4.6% of codespace creation requests. The second period was more pronounced, peaking at approximately 30% of codespace creation requests in the most-affected region before recovery. Both periods were caused by an unexpected surge in codespace creation from an abusive actor that drained the available compute capacity in the affected regions faster than it could be replenished. \u003cbr /\u003e\u003cbr /\u003eWe mitigated the impact by identifying and stopping the sources of the excess creation volume, reducing the resources that could be consumed in the affected regions, and rebalancing traffic across regions to restore capacity. Codespace creation success rates returned to normal after each period. \u003cbr /\u003e\u003cbr /\u003eWe are working to add automated, low-latency controls to throttle abnormal codespace creation and to strengthen our detection and safeguards, so we can reduce our time to detection and mitigation of issues like this in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e14\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e08:21\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e09:56\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;q27ttsnp0x4g&quot;,&quot;name&quot;:&quot;Actions runs are experiencing failures to start&quot;,&quot;message&quot;:&quot;On July 13, 2026, between 13:11 and 13:53 UTC, some customers experienced failures starting and running GitHub Actions workflows, which also affected Copilot cloud agent sessions and GitHub Pages builds since they depend on Actions. During the peak of the incident, 30% of Actions jobs failed to start and 2% were delayed more than 5 minutes. \u003cbr /\u003e\u003cbr /\u003eThe incident was triggered by a configuration change in an internal autoscaling component that contained outdated capacity threshold values. This caused a critical Actions service to scale below its required baseline, reducing capacity for workflow processing. We identified the regression, rolled back the change, and restored service capacity. New workflow executions recovered by 13:39 UTC. Full recovery was reached by 13:53 UTC after the queued backlog was drained. \u003cbr /\u003e\u003cbr /\u003eTo prevent recurrence, we have added deployment guardrails to validate that autoscaling inputs are current and to detect drift between planned and live scaling state before autoscaling changes are applied.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e13\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e13:32\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e13:53\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;cstx3v63mklm&quot;,&quot;name&quot;:&quot;Delays starting Actions runs&quot;,&quot;message&quot;:&quot;On July 9, 2026, between 03:29 UTC and 13:39 UTC, GitHub Actions experienced delayed and failed job starts on GitHub-hosted runners. The incident was caused by an unhealthy state in a backend data service responsible for provisioning hosted runners, preventing runner acquisition for a subset of workloads. During most of the incident, approximately 8% of workflow runs on hosted runners were delayed by more than 5 minutes, while roughly 2% failed to start.\u003cbr /\u003e\u003cbr /\u003eAt 13:39 UTC, we restored the health of the backend data replication system, allowing provisioning to recover and the accumulated workflow backlog to drain. Service performance then returned to expected levels. We are improving provisioning-service resiliency, workload distribution, and capacity balancing to reduce the likelihood and impact of similar incidents.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e9\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e04:34\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e13:52\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;fz9sdc2q008p&quot;,&quot;name&quot;:&quot;Actions and Codespaces APIs experiencing partial failures&quot;,&quot;message&quot;:&quot;On July 7, 2026, between 14:01 UTC and 16:17 UTC the Actions and Codespaces REST APIs were degraded and returned intermittent 500-class errors for a percentage of requests. Error rates peaked at approximately 8% of Actions runner API requests and 13% of Codespaces API requests, though retries were frequently successful. In-progress Actions runs and Codespaces were not impacted and continued successfully. This was due to a recent change that did not deliver the expected performance and, under certain conditions, caused downstream errors.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by rolling back the change, after which the affected services recovered.\u003cbr /\u003e\u003cbr /\u003eWe are working to improve the resilience of our services to these conditions and to strengthen our monitoring to reduce our time to detection and mitigation of issues like this one in the future.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e7\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:14\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e16:17\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;5bnwwg9tzd4q&quot;,&quot;name&quot;:&quot;Incident with Pages&quot;,&quot;message&quot;:&quot;On July 2nd, 2026, between approximately 15:00 and 18:30 UTC, the GitHub Pages service experienced degraded deployment performance due to a surge in demand that exceeded available processing capacity. During this period, users publishing to GitHub Pages may have seen their deployments queued or taking substantially longer than usual to go live. No other GitHub services were impacted.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by scaling up Pages deployment workers and provisioning additional storage capacity to clear the backlog.\u003cbr /\u003e\u003cbr /\u003eGitHub is reviewing capacity planning and autoscaling measures to reduce the likelihood of similar delays in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e2\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e16:54\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:25\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;rl7f90w0n0gq&quot;,&quot;name&quot;:&quot;Delays in copilot budget limits resets for some users&quot;,&quot;message&quot;:&quot;On July 1, 2026, between approximately 00:00 UTC and 13:04 UTC, some GitHub Copilot customers whose budget was exhausted before the monthly reset remained incorrectly blocked from paid Copilot usage after the new billing month began, even though their budgets had reset. Some budget changes also took longer than usual to apply. Only customers with an exhausted budget were affected, which limited the impact.\u003cbr /\u003e\u003cbr /\u003eThis was caused by a caching issue at the monthly reset: for some users, a pre-reset \&quot;budget exhausted\&quot; status was re-saved and served even though their budget had reset, so they stayed blocked. We had built a safeguard ahead of the reset to prevent this, but it did not take effect because an internal configuration service did not load its settings correctly. We resolved the incident by deploying a change that discards the outdated status and recomputes access from current budget data independently of that configuration, and by working through the backlog of budget updates.\u003cbr /\u003e\u003cbr /\u003eTo prevent recurrence, we are ensuring pre-reset status cannot survive the monthly budget reset, adding alerting for this failure mode, and increasing capacity to absorb the monthly surge of budget updates.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jul \u003cvar data-var=&#39;date&#39;\u003e1\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e10:51\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e13:26\u003c/var\u003e UTC&quot;}]},{&quot;name&quot;:&quot;June&quot;,&quot;year&quot;:2026,&quot;starts_on&quot;:1,&quot;days&quot;:30,&quot;incidents&quot;:[{&quot;code&quot;:&quot;mc4yx9f8x1hk&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services - Signup Flow&quot;,&quot;message&quot;:&quot;Between 15:19 UTC and 15:49 UTC on June 30, 2026, users were unable to complete the signup flow for GitHub.com/signup. Approximately 62% of new user signups failed for about 30 minutes during this window.\u003cbr /\u003e\u003cbr /\u003eThis was caused by a configuration change to the signup flow that unintentionally blocked users from completing signup.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by reverting the change, which restored successful signups. To reduce the likelihood and impact of similar issues, we are adopting staged, incremental rollouts for changes on the signup path, improving our ability to test these changes before they reach production, and adding checks to verify signup health before and during any change that affects this flow.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e30\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:38\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e15:49\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;0rkjjs2ssp7z&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;From June 26, 2026 at 23:40 UTC through June 28, 2026 at 20:55 UTC, Copilot Cloud Agent was degraded. The agent could fail when reporting progress, replying to pull request comments, or opening pull requests. For affected built-in tool calls, the average error rate was approximately 8%, with hourly error rates peaking around 26%.\u003cbr /\u003e\u003cbr /\u003eThis was due to a regression introduced during a Copilot Cloud Agent runtime deployment that caused several built-in agent tools to become unavailable. In many cases, the affected tool calls failed silently so agent jobs appeared to succeed. This monitoring gap meant it took longer than expected to identify the failure. We mitigated the incident by reverting the runtime deployment to the previously stable version.\u003cbr /\u003e\u003cbr /\u003eWe&#39;ve added monitoring and alerting for this class of tool-availability error to reduce time-to-detection. We&#39;re also adding regression tests for these built-in agent tools, and improving the shipping safety for future runtime rollouts to avoid similar issues.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e28\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e17:50\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e20:55\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;v0b3bpsyvqtk&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;This incident was used to notify for a maintenance event. There is no specific root cause analysis. Work progressed as planned without any issues to report.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e27\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e14:02\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e20:33\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;9ndxtnrwjf37&quot;,&quot;name&quot;:&quot;Degradation with Webhooks, Pull Requests and Actions&quot;,&quot;message&quot;:&quot;On June 25, 2026, between 17:33 UTC and 17:55 UTC, our background job service experienced degradation which increased delays to pull requests, repository pushes, Actions workflows, and Webhooks, with delays peaking at 7m. The issue was caused by underlying hypervisor issues and an incoming traffic spike, causing service timeouts which led to a connection storm and continual rebalances. \u003cbr /\u003e\u003cbr /\u003eThe issue was mitigated by replacing the problem node at 17:49, after which all services saw recovery by 18:07.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e25\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e17:50\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:27\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;9n670kvk0vw9&quot;,&quot;name&quot;:&quot;We are seeing elevated errors with Next Edit Suggestions and Completions&quot;,&quot;message&quot;:&quot;On June 23, 2026, between 22:45 and 23:29 UTC, GitHub Copilot Completions and Next Edit Suggestions were degraded for users in all regions. During this window, affected users may have seen failed or missing code completions and Next Edit Suggestions. On average about 25% of Completions and Next Edit Suggestions requests failed during the impact window, peaking at roughly 27%. The cause was a configuration change that prevented the Copilot service from obtaining the authentication tokens it needs to reach its model backends; this both failed requests directly and caused the service to temporarily remove backends from rotation. GitHub engineers detected the elevated error rate within minutes, declared an incident, and mitigated the issue at 23:22 UTC by redeploying the service with a known-good configuration, which restored normal operation. As a follow-up, the team disabled the affected authentication path to prevent a future deployment from re-introducing the problem, and is making the change rollout safer. We apologize for the disruption and are taking steps to reduce the likelihood of similar incidents.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e23\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e23:04\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e23:29\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;5t81zk0vrk3z&quot;,&quot;name&quot;:&quot;Disruption with Copilot next edit suggestions&quot;,&quot;message&quot;:&quot;On June 17, 2026, between 16:57 UTC and 19:14 UTC, Copilot code completions were degraded and users were unable to receive Next Edit Suggestions. Standard ghost text code completions were not affected. This was due to a configuration change that caused the service&#39;s routing layer to incorrectly discard all Next Edit Suggestion model endpoints as invalid.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by deploying a corrected configuration change at 18:55 UTC, with full recovery observed at 19:14 UTC.\u003cbr /\u003e\u003cbr /\u003eWe are working to improve the resilience of our routing layer to limit impact due to a subset of invalid configurations, and to improve our alerting to detect sudden traffic changes that are not captured by standard error rate monitors.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e17\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e17:57\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e19:28\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;kn7gv3tlfc54&quot;,&quot;name&quot;:&quot;Incident With Webhooks&quot;,&quot;message&quot;:&quot;On June 17, 2026, between 11:35 UTC and 19:20 UTC, the Webhooks service was degraded and delivered webhook payloads with missing installation information. On average, 11.3% of webhook deliveries were impacted. Customers relying on the installation field for authentication or routing were unable to process affected webhooks. A smaller subset of deliveries for the security_advisory event (0.04%) were delivered successfully but were not recorded for redelivery. This was due to a defect in a new delivery code path that failed to include installation data in webhook payloads.\n\nWe mitigated the incident by disabling the feature flag controlling the new code path.\n\nWe are working to improve our automated validation of webhook payloads, and introduce automated alerting for webhook payload regressions to reduce our time to detection and mitigation of issues like this one in the future.\n\nThe following events were affected: branch_protection_configuration, code_scanning_alert, commit_comment, custom_property, custom_property_values, dependabot_alert, deploy_key, deployment_protection_rule, deployment_review, dismissal_request_code_scanning, dismissal_request_secret_scanning, installation_target, member, membership, merge_queue_entry, org_block, organization, projects_v2, projects_v2_item, pull_request_review_thread, repository_ruleset, secret_scanning_alert, secret_scanning_alert_location, secret_scanning_scan, security_and_analysis, star, sub_issues, team, team_add, workflow_job.&quot;,&quot;impact&quot;:&quot;none&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e17\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e19:00\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e19:00\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;rfmjwng33vjf&quot;,&quot;name&quot;:&quot;Incident with Copilot Availability&quot;,&quot;message&quot;:&quot;On June 17, 2026, between approximately 03:35 UTC and 04:44 UTC, GitHub Copilot was degraded and most of its frontier chat models were temporarily unavailable across all regions. During this window, affected models either disappeared from the model picker in the web, editor, and CLI experiences, or returned a \&quot;model not available\&quot; error when selected. Customers could continue using GitHub Copilot by selecting one of the models that remained available. The incident occurred during off-peak hours, which limited the number of customers affected.\u003cbr /\u003e\u003cbr /\u003eThis was due to a configuration change that our production system deemed invalid. We mitigated the incident by reverting the configuration change, after which the affected models returned automatically as the service reloaded the previous configuration.\u003cbr /\u003e\u003cbr /\u003eWe are working to roll out configuration changes gradually with stronger validations, alerts on sudden drops in the number of available models, and automatically rolls back configuration changes that produce these alerts.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e17\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e03:50\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e04:44\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;1s444p9sf9wg&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;On June 16, 2026, between 17:20 UTC and 18:15 UTC, the Opus 4.8 model experienced degraded availability in GitHub Copilot. During this window, some requests to Opus 4.8 failed or errored. Other Copilot models were not affected and remained available as alternatives. This was caused by an issue with an upstream model provider. The upstream provider resolved the issue, and we monitored Opus 4.8 until success rates returned to normal. The incident is fully resolved.&quot;,&quot;impact&quot;:&quot;major&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e16\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e17:45\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:15\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;d9b4dsg8d0r6&quot;,&quot;name&quot;:&quot;Multiple services have elevated errors and endpoint failures when checking feature flags&quot;,&quot;message&quot;:&quot;Between 17:38 UTC and 18:22 UTC on June 15, 2026, approximately 83% of requests to the analytics endpoint serving the /chronicle feature failed.  The cause was an internal feature-flag service that encountered a transient error and failed to recover, causing feature flag checks to fail. The analytics endpoint was gated behind one of these flags, resulting in requests being rejected. We restored service health by removing the feature flag gating the analytics endpoint and deploying that change. To avoid recurrence of similar incidents, we have changed the feature-flag client so that errors that are not known to be permanent are retried, and we are improving alerting and startup behavior so this class of failure is detected and recovered from faster.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e15\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e18:32\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e19:10\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;67w72l5v25x3&quot;,&quot;name&quot;:&quot;Increased latency with webhooks&quot;,&quot;message&quot;:&quot;On June 15, 2026, between 15:27 UTC and 16:23 UTC, GitHub webhook deliveries were delayed. During this window, webhook events were delivered later than normal, with average end-to-end delivery latency peaking at approximately 8.8 minutes. No webhook deliveries were lost — delayed events were queued and delivered once processing recovered.\u003cbr /\u003e\u003cbr /\u003eThis was caused by a temporary throughput constraint in an internal event-processing system that moves webhook events through GitHub&#39;s delivery pipeline. The rate at which events were processed for delivery dropped below the incoming volume, creating a backlog. We restarted the affected pipeline service, after which throughput recovered and the backlog fully drained by approximately 16:29 UTC. Webhook delivery latency returned to normal, the incident was mitigated at 16:39 UTC, and fully resolved at 17:37 UTC.\u003cbr /\u003e\u003cbr /\u003eTo reduce the likelihood and impact of similar incidents, we are working on improving the accuracy of the utilization metrics used to scale our delivery worker pools, reviewing connection and capacity headroom in the delivery pipeline.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e15\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:37\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e17:37\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;4yz3c18qmdxn&quot;,&quot;name&quot;:&quot;Incident with Webhooks&quot;,&quot;message&quot;:&quot;On June 11, 2026, between 19:28 UTC and 21:06 UTC, GitHub webhook deliveries were delayed. Average delivery latency peaked at approximately 3.4 minutes, with some deliveries delayed by as much as 62 minutes at the 99th percentile. No events were lost — delayed events were queued and delivered once processing caught up.\u003cbr /\u003e\u003cbr /\u003eThis was due to a change in how webhook traffic was distributed across regions: to relieve load on one region, a portion of processing was shifted to another, where higher latency prevented our delivery workers from keeping pace with incoming volume, creating a backlog. We mitigated the incident by rebalancing webhook traffic distribution; as load returned to normal levels, processing caught up and the delivery backlog fully drained.\u003cbr /\u003e\u003cbr /\u003eWe are working on improving the accuracy of the utilization metrics used to scale our delivery worker pools, and reassess how we distribute webhook traffic across regions, to reduce our time to detection and mitigation of issues like this one in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e11\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e19:42\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e22:19\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;fcj3088jg1wx&quot;,&quot;name&quot;:&quot;Authentication issues related to API requests&quot;,&quot;message&quot;:&quot;Between 15:05 UTC and 16:25 UTC, GitHub API services experienced degraded availability due to sporadic authentication failures affecting approximately 9% of requests. Customers experienced intermittent \&quot;logged out\&quot; behavior as erroneous 401 responses triggered repeated authentication flows in app integrations. Affected requests also experienced approximately 800ms of additional latency.   \u003cbr /\u003e\u003cbr /\u003eA memcached proxy service rollout to our internal API infrastructure caused our authentication service to pick up an incorrect memcached host configuration, leading to intermittent authentication lookup failures. We mitigated the incident by deploying a configuration change to memcached to use the correct host. \u003cbr /\u003e\u003cbr /\u003eTo prevent similar issues in the future, we plan to migrate our authentication system to the new memcached infrastructure to improve resilience and strengthen overall reliability posture.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e10\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:20\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e16:39\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;jpd6l1jq0r54&quot;,&quot;name&quot;:&quot;Degraded availability for GitHub.com, GraphQL API, and Webhooks UI/API&quot;,&quot;message&quot;:&quot;On June 8, 2026, between 14:49 and 14:54 UTC, a subset of requests to GitHub.com, the REST API, GraphQL API, and Webhooks UI/API experienced elevated error rates due to a transient infrastructure capacity issue that self-resolved within approximately 5 minutes.\n\nUsers experienced HTTP 500 errors and timeouts when accessing GitHub.com, the REST API, GraphQL API, and Webhooks UI/API for approximately 5 minutes, with the REST API taking up to 12 minutes to fully recover.&quot;,&quot;impact&quot;:&quot;none&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e8\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:00\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e15:00\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;71hv2q6tk693&quot;,&quot;name&quot;:&quot;Disruption with Claude Opus 4.7&quot;,&quot;message&quot;:&quot;On June 8, 2026, between 08:40 UTC and 09:30 UTC, the Claude Opus 4.7 model experienced degraded availability with error rates peaking at 8.4% and averaging 1.9%. This was due to an upstream provider issue that caused temporary unavailability and rate limiting on secondary failover systems. Users selecting Auto or alternative models were unaffected. We are improving provider failover mechanisms and monitoring to prevent similar issues.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e8\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e09:05\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e10:03\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;m7n7sm0sr1pz&quot;,&quot;name&quot;:&quot;Pull Requests and Issues unavailable for signed-out users&quot;,&quot;message&quot;:&quot;On June 8, 2026, between approximately 06:30 UTC and 08:36 UTC, signed-out users experienced sustained elevated HTTP 504 errors when accessing Pull Requests, Issues, releases, patch diffs, and other related GitHub.com pages. During the incident, approximately 17% of unauthenticated requests to the affected GitHub.com endpoints returned gateway timeout errors, peaking at roughly 34% of requests at around 06:50 UTC. Some GitHub Actions workflows were also affected when they depended on release downloads or related GitHub.com endpoints. The impact lasted approximately two hours and was isolated to unauthenticated traffic; signed-in users were not affected. \u003cbr /\u003e\u003cbr /\u003eThe issue was caused by a significant increase in abusive traffic to specific GitHub.com endpoints. This degraded our ability to respond to unauthenticated requests, causing requests to queue beyond timeout thresholds and return gateway timeout errors. \u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by identifying the anomalous traffic pattern and applying targeted blocks at the load balancer and application layers. Error rates returned to normal and affected services were fully restored by 08:36 UTC. \u003cbr /\u003e\u003cbr /\u003eTo reduce the likelihood and impact of similar incidents in the future, we are improving automated detection and blocking for these traffic patterns, improving our emergency traffic-blocking deployment path, and evaluating routing changes for endpoints used by both signed-out users and automated workflows.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e8\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e07:11\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e08:36\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;4843jm0lsls6&quot;,&quot;name&quot;:&quot;EU Network Maintenance&quot;,&quot;message&quot;:&quot;This incident was used to notify for a maintenance event. There is no specific root cause analysis. Maintenance did run longer than expected (we were complete at 18:48 UTC) but the work proceeded as planned.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e6\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:31\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e18:49\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;b0plzff6yl6f&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services in the EU region&quot;,&quot;message&quot;:&quot;On June 6, 2026 between 16:18 UTC and 17:01 UTC, users experienced elevated error rates when performing Git operations (cloning, fetching, downloading archives) and accessing package registries. The issue affected users whose traffic was routed through our European infrastructure.\u003cbr /\u003e\u003cbr /\u003eDuring this time, on average 0.95% of Codeload requests and 9.2% of Package Registry requests failed with server errors. At peak, the Codeload error rate reached 1.76% and Package Registry errors reached 27%.\u003cbr /\u003e\u003cbr /\u003eThe root cause was a planned network circuit migration that disrupted connectivity at one of our points of presence. Our process for shifting traffic away from the site did not operate as expected, resulting in a small amount of production traffic to continue being serviced at the effected site during the maintenance window. The issue was mitigated by rolling back the network change, restoring normal connectivity. Services fully recovered by 17:01 UTC.\u003cbr /\u003e\u003cbr /\u003eTo reduce the likelihood of similar incidents in the future, we are reviewing our site drain process to make it more verbose and add visibility so any unexpected behavior is caught earlier.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e6\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e16:53\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e17:07\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;2nmfnbknhlnv&quot;,&quot;name&quot;:&quot;Auth issue resulting in API impacts, including some Slack and Teams channel subscriptions&quot;,&quot;message&quot;:&quot;On June 5, 2026, between 15:35 UTC and 16:45 UTC, 0.11% of authenticated REST API requests incorrectly returned “not found” responses. Impact was concentrated among - and significantly higher for - users authenticating with user-to-server tokens to access organization-owned repositories.\u003cbr /\u003e\u003cbr /\u003eSome users of our GitHub for Slack and GitHub for Microsoft Teams integrations saw their channel subscriptions removed as those systems interpreted the transient \&quot;not found\&quot; response as durable loss of access. Roughly 12% of organizations with active channel subscriptions were impacted, with ~2% of all channel subscriptions being removed.\u003cbr /\u003e\u003cbr /\u003eThese issues were triggered by a change to an internal authorization component that did not correctly resolve access for user-to-server tokens against organization-owned repositories. We mitigated the incident by disabling the accompanying feature flag at 16:45 UTC, after which API responses returned to normal. We then restored all impacted Slack and Microsoft Teams channel subscriptions, with restoration completed at 22:21 UTC.\u003cbr /\u003e\u003cbr /\u003eWe are working to add retry and grace-period logic in the chat integrations so transient errors no longer trigger subscription deletions. In parallel, we are improving observability and gating of authorization changes so downstream impact is detected during scoped, gradual rollouts.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e5\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e17:20\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e22:21\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;5h5lmbffp07c&quot;,&quot;name&quot;:&quot;Copilot Code Review Failing&quot;,&quot;message&quot;:&quot;On June 4, 2026, from 17:30 UTC to 18:55 UTC, Copilot Code Review experienced elevated failures for review requests on GitHub.com. Affected users saw “Copilot ran into an error” on pull requests when requesting a code review.\u003cbr /\u003e\u003cbr /\u003eDuring the incident window, an average of 81.6% of Copilot Code Review requests failed, with a peak failure rate of 93.9%. Approximately 36,800 code review requests failed. GitHub Enterprise Cloud with data residency was not impacted.\u003cbr /\u003e\u003cbr /\u003eThe issue was caused by a newly released dependency used by the Copilot Code Review processing workflow. The release introduced an incompatibility with the runtime environment. Because the workflow automatically consumed the latest release, the incompatible version was picked up without sufficient compatibility validation and caused review processing to fail.\u003cbr /\u003e\u003cbr /\u003eWe mitigated the incident by removing the problematic dependency version and redeploying the affected processing service. New code reviews began recovering at 18:44 UTC, and the failure rate returned to baseline by 18:55 UTC. Remaining timed-out work drained by 19:59 UTC.\u003cbr /\u003e\u003cbr /\u003eTo reduce the risk of recurrence, we are pinning the dependency version instead of automatically consuming the latest release, adding compatibility checks for future releases, improving fast-failure behavior when the review processor cannot start, adding shorter timeout controls for review workflows, and improving monitoring for review completion failures.&quot;,&quot;impact&quot;:&quot;critical&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e4\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e18:02\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e19:59\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;tf25qs8wdw5h&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;Between June 1, 2026, 23:00 UTC and June 4, 2026 04:11 UTC, customers experienced delays in Dependabot scheduled version updates.  \u003cbr /\u003e\u003cbr /\u003ePull request creation for version updates was delayed, with delays increasing over time and reaching up to two days. Approximately 1.5 million repositories with active Dependabot version update configurations were affected. Dependabot security updates were not affected. The primary cause was changes to an internal platform service that routes requests for Dependabot and other services. \u003cbr /\u003e \u003cbr /\u003eWe mitigated the incident by deploying a fix that enables batch enqueuing of update jobs, which significantly increased processing throughput. Once the backlog was drained, Dependabot returned to normal processing times. \u003cbr /\u003e \u003cbr /\u003eTo reduce the risk of recurrence, we are working on tuning batch size and concurrency limits for Dependabot update job processing. We are also adding monitoring for job processing lag to enable earlier detection and faster mitigation of similar issues.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e3\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e19:42\u003c/var\u003e - Jun \u003cvar data-var=&#39;date&#39;\u003e4\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e04:11\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;j240y90h4g0r&quot;,&quot;name&quot;:&quot;Disruption with some GitHub services&quot;,&quot;message&quot;:&quot;On June 2, 2026, between 21:54 UTC and June 3, 2026 06:45 UTC, the Spark service was degraded and users were unable to store or retrieve data for their Spark apps in one of our hosting regions. Users could still make changes to their app configuration during this time. The error rate peaked at 25% of affected requests to the service. Impact was limited to users whose requests were served through a single affected region; 43 users experienced errors during this window.\u003cbr /\u003e\u003cbr /\u003eThe root cause was a configuration that referenced a service component by a fixed address rather than a dynamic service endpoint. When the component was replaced, requests could no longer reach the fixed address and began to fail. We resolved the incident by updating the configuration to use a our standard service endpoints that are resilient to component replacement. Recovery time was extended because replacing the component required overrides to a temporary deployment safeguard.\u003cbr /\u003e\u003cbr /\u003eWe are working to add validation that prevents fixed infrastructure addresses from being used in application configuration outside of test environments and to improve our monitoring to reduce our time to detect.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e3\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e03:13\u003c/var\u003e - \u003cvar data-var=&#39;time&#39;\u003e06:46\u003c/var\u003e UTC&quot;},{&quot;code&quot;:&quot;5wdgxw2rvbt3&quot;,&quot;name&quot;:&quot;Delays with Code Scanning and Billing&quot;,&quot;message&quot;:&quot;Starting from 13:00 UTC June 1, 2026, to 00:17 UTC June 2, 2026, multiple services experienced delayed job processing due to increased latency in our background job queue service. The root cause was insufficient queue processing capacity to handle a large week-over-week increase in total job traffic.\u003cbr /\u003e\u003cbr /\u003eUsers saw up to 90 minutes of delay in billing usage updates, 30 minutes of delay for webhook notifications to show, and 15 minutes of delay to see email notifications. Mitigation involved scaling up our background job service capacity to handle the spike in job traffic.\u003cbr /\u003e\u003cbr /\u003eWe have added queue capacity monitoring to our background job queue service to stay ahead of weekly growth patterns and to reduce time to detect in the future.&quot;,&quot;impact&quot;:&quot;minor&quot;,&quot;timestamp&quot;:&quot;Jun \u003cvar data-var=&#39;date&#39;\u003e1\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e15:17\u003c/var\u003e - Jun \u003cvar data-var=&#39;date&#39;\u003e2\u003c/var\u003e, \u003cvar data-var=&#39;time&#39;\u003e00:17\u003c/var\u003e UTC&quot;}]}],&quot;show_component_filter&quot;:false,&quot;show_uptime_calendar&quot;:true,&quot;component_filter&quot;:null,&quot;start_time&quot;:&quot;2026-06-01T00:00:00Z&quot;,&quot;end_time&quot;:&quot;2026-08-31T23:59:59Z&quot;}"></div>

    <div class="page-footer border-color font-small">
  <a href="/" aria-label="Back to current status">
    <span class="current-status-arrow">&larr;</span> Current Status
  </a>
  <span class="color-secondary powered-by"><a class="color-secondary" target="_blank" rel="noopener noreferrer nofollow" href="https://www.atlassian.com/software/statuspage?utm_campaign=www.githubstatus.com&amp;utm_content=SP-notifications&amp;utm_medium=powered-by&amp;utm_source=inapp">Powered by Atlassian Statuspage</a></span>
</div>

  </div>


  
</div>


    <script src="https://dka575ofm4ao0.cloudfront.net/assets/status_manifest-9c64d4a1ecaac09c5c1685949fa820bec1cb910c467fa2b0b4a14ed8d82838f8.js"></script>
    <div id="cpt-notification-container"></div>
    




    <!-- all of the content_for stuff -->
      <script src="https://dka575ofm4ao0.cloudfront.net/assets/register_subscription_form-589b657fec607087fc5c740c568270907310bc4f6aaa20256e70f01b103025ca.js"></script>

  <script type="text/javascript">
      $(function() {
          SP.currentPage.registerSubscriptionForm('email');

          SP.currentPage.registerSubscriptionForm('sms');

          SP.currentPage.registerSubscriptionForm('webhook');

      });





  </script>
    <script src="https://dka575ofm4ao0.cloudfront.net/assets/status_common-a86dffb81955091741c3de8bded6ce66ae0c6d8f736b57b580f853d9f892727e.js"></script>
      <div class="custom-footer-container">
    <div class="footer mt-6 border-top" role="contentinfo">
  <img src="https://user-images.githubusercontent.com/19292210/60553864-044dd200-9cea-11e9-996a-a7a316ec3a35.png"
    class="illo-mobile-footer" alt="GitHub footer">

  <div class="container-lg p-responsive">
    <div class="d-flex flex-wrap py-5 mb-5">
      <section class="col-12 col-lg-4 mb-5">
        <a href="https://github.com/" data-ga-click="Footer, go to GitHub, text:GitHub" class="text-gray-dark"
          aria-label="GitHub text logo">
          <svg class="octicon octicon-logo-github" width="90" height="32" viewBox="0 0 416 95" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <g clip-path="url(#clip0_730_27128)">
              <path
                d="M41.6394 69.3848C29.0066 67.8535 20.1062 58.7617 20.1062 46.9902C20.1062 42.2051 21.8289 37.0371 24.7 33.5918C23.4558 30.4336 23.6472 23.7344 25.0828 20.959C28.9109 20.4805 34.0789 22.4902 37.1414 25.2656C40.7781 24.1172 44.6062 23.543 49.2957 23.543C53.9851 23.543 57.8132 24.1172 61.2585 25.1699C64.2253 22.4902 69.489 20.4805 73.3171 20.959C74.657 23.543 74.8484 30.2422 73.6042 33.4961C76.6667 37.1328 78.2937 42.0137 78.2937 46.9902C78.2937 58.7617 69.3933 67.6621 56.5691 69.2891C59.823 71.3945 62.0242 75.9883 62.0242 81.252L62.0242 91.2051C62.0242 94.0762 64.4167 95.7031 67.2878 94.5547C84.6101 87.9512 98.2 70.6289 98.2 49.1914C98.2 22.1074 76.1882 6.69539e-07 49.1042 4.309e-07C22.0203 1.92261e-07 0.199951 22.1074 0.199951 49.1914C0.199951 70.4375 13.6941 88.0469 31.8777 94.6504C34.4617 95.6074 36.95 93.8848 36.95 91.3008L36.95 83.6445C35.6101 84.2188 33.8875 84.6016 32.3562 84.6016C26.0398 84.6016 22.3074 81.1563 19.6277 74.7441C18.575 72.1602 17.4265 70.6289 15.2253 70.3418C14.0769 70.2461 13.6941 69.7676 13.6941 69.1934C13.6941 68.0449 15.6082 67.1836 17.5222 67.1836C20.2976 67.1836 22.6902 68.9063 25.1785 72.4473C27.0925 75.2227 29.1023 76.4668 31.4949 76.4668C33.8875 76.4668 35.4187 75.6055 37.6199 73.4043C39.2468 71.7773 40.491 70.3418 41.6394 69.3848Z"
                fill="#24292e" />
              <g clip-path="url(#clip1_730_27128)">
                <path
                  d="M188.937 83.0045L188.937 33.2827L202.915 33.2827L202.915 83.0045L188.937 83.0045ZM230.016 83.0045C220.727 83.0045 217.099 79.0232 217.099 70.6183L217.099 44.9611L208.252 44.9611L208.252 33.2827L217.099 33.2827L217.099 23.3737L231.078 20.1002L231.078 33.2827L241.429 33.2827L241.429 44.9611L231.078 44.9611L231.078 67.5217C231.078 70.2644 232.317 71.3261 235.059 71.3261L241.429 71.3261L241.429 83.0045L230.016 83.0045ZM327.47 83.8892C316.588 83.8892 310.66 77.8731 310.66 66.9024L310.66 33.2827L324.728 33.2827L324.728 63.1866C324.728 69.2912 327.47 72.6532 332.69 72.6532C338.706 72.6532 343.307 67.0794 343.307 59.4707L343.307 33.2827L357.374 33.2827L357.374 83.0045L343.307 83.0045L343.307 74.5996C340.653 79.9964 334.283 83.8892 327.47 83.8892ZM394.613 83.8892C387.832 83.8892 381.639 79.9964 378.687 74.4226L378.687 83.0045L364.709 83.0045L364.709 13.6417L378.776 13.6417L378.776 42.3954C381.639 36.3792 388.098 32.1325 394.613 32.1325C408.181 32.1325 415.348 41.5107 414.873 58.0551C415.348 74.4226 407.916 83.8892 394.613 83.8892ZM389.658 72.1223C396.945 72.1223 400.926 66.7255 400.452 58.0551C400.926 49.2963 396.945 43.8994 389.658 43.8994C383.851 43.8994 379.251 49.5617 378.776 57.3473L378.776 58.1436C379.251 66.1946 383.851 72.1223 389.658 72.1223ZM288.734 13.6417L288.734 41.7761L262.369 41.7761L262.369 13.6417L247.329 13.6417L247.329 83.0045L262.369 83.0045L262.369 55.224L288.734 55.224L288.734 83.0045L303.775 83.0045L303.775 13.6417L288.734 13.6417ZM150.628 84.3316C130.102 84.3316 117.185 70.2644 117.185 48.2346C117.185 26.2048 130.368 12.3146 151.247 12.3146C168.234 12.3146 178.497 19.5693 181.77 31.7786L166.553 35.406C164.695 28.7705 159.387 25.1431 151.247 25.1431C139.126 25.1431 132.579 33.1057 132.579 48.2346C132.579 63.3635 138.949 71.503 150.893 71.503C161.864 71.503 168.411 64.7791 168.411 53.366L168.411 50.7119L172.304 56.1087L149.655 56.1087L149.655 43.3686L183.628 43.3686L183.628 51.4196C183.628 72.5647 171.331 84.3316 150.628 84.3316ZM195.926 28.5936C200.615 28.5936 204.243 24.9662 204.243 20.2771C204.243 15.5881 200.615 11.9607 195.926 11.9607C191.237 11.9607 187.61 15.5881 187.61 20.2771C187.61 24.9662 191.237 28.5936 195.926 28.5936Z"
                  fill="#24292e" />
              </g>
            </g>
            <defs>
              <clipPath id="clip0_730_27128">
                <rect width="416" height="95" fill="white" />
              </clipPath>
              <clipPath id="clip1_730_27128">
                <rect width="298.068" height="75.9408" fill="white" transform="translate(117.185 9.49258)" />
              </clipPath>
            </defs>
          </svg>
        </a>

        <h3 class="h5 mt-4 mb-0" id="subscribe-to-newsletter">Subscribe to our developer newsletter</h3>
        <p class="f5 color-fg-muted mb-3">Get tips, technical guides, and best practices. Twice a month. Right in your
          inbox.</p>
        <a href="https://resources.github.com/newsletter/" class="btn btn-muted mb-4">Subscribe</a>
      </section>

      <nav class="col-6 col-sm-3 col-lg-2 mb-6 mb-md-2 pr-3 pr-lg-0 pl-lg-4" aria-labelledby="footer-title-product">
        <h3 class="h5 mb-3 text-mono color-fg-muted text-normal" id="footer-title-product">Product</h3>
        <ul class="list-style-none color-fg-muted f5">
          <li class="lh-condensed mb-3"><a href="https://github.com/features"
              data-ga-click="Footer, go to features, text:features" class="link-gray">Features</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/enterprise"
              data-ga-click="Footer, go to enterprise, text:enterprise" class="link-gray">Enterprise</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/features/copilot"
              data-ga-click="Footer, go to copilot, text:copilot" class="link-gray">Copilot</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/security"
              data-ga-click="Footer, go to security, text:security" class="link-gray">Security</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/pricing"
              data-ga-click="Footer, go to pricing, text:pricing" class="link-gray">Pricing</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/team" data-ga-click="Footer, go to team, text:team"
              class="link-gray">Team</a></li>
          <li class="lh-condensed mb-3"><a href="https://resources.github.com"
              data-ga-click="Footer, go to resources, text:resources" class="link-gray">Resources</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/github/roadmap"
              data-ga-click="Footer, go to roadmap, text:roadmap" class="link-gray">Roadmap</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/resources/articles/devops-tools-comparison"
              data-ga-click="Footer, go to compare, text:compare" class="link-gray">Compare GitHub</a></li>
        </ul>
      </nav>

      <nav class="col-6 col-sm-3 col-lg-2 mb-6 mb-md-2 pr-3 pr-md-0 pl-md-4" aria-labelledby="footer-title-platform">
        <h3 class="h5 mb-3 text-mono color-fg-muted text-normal" id="footer-title-platform">Platform</h3>
        <ul class="list-style-none f5">
          <li class="lh-condensed mb-3"><a
              href="https://docs.github.com/get-started/exploring-integrations/about-building-integrations"
              data-ga-click="Footer, go to api, text:api" class="link-gray">Developer API</a></li>
          <li class="lh-condensed mb-3"><a href="https://partner.github.com"
              data-ga-click="Footer, go to partners, text:partners" class="link-gray">Partners</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/edu"
              data-ga-click="Footer, go to education, text:education" class="link-gray">Education</a></li>
          <li class="lh-condensed mb-3"><a href="https://cli.github.com"
              data-ga-click="Footer, go to github cli, text:cli" class="link-gray">GitHub CLI</a></li>
          <li class="lh-condensed mb-3"><a href="https://desktop.github.com"
              data-ga-click="Footer, go to github desktop, text:desktop" class="link-gray">GitHub Desktop</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/mobile"
              data-ga-click="Footer, go to github mobile, text:mobile" class="link-gray">GitHub Mobile</a></li>
        </ul>
      </nav>

      <nav class="col-6 col-sm-3 col-lg-2 mb-6 mb-md-2 pr-3 pr-md-0 pl-md-4" aria-labelledby="footer-title-support">
        <h3 class="h5 mb-3 text-mono color-fg-muted text-normal" id="footer-title-support">Support</h3>
        <ul class="list-style-none f5">
          <li class="lh-condensed mb-3"><a href="https://docs.github.com" data-ga-click="Footer, go to docs, text:docs"
              class="link-gray">Docs</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.community"
              data-ga-click="Footer, go to community, text:community" class="link-gray">Community Forum</a></li>
          <li class="lh-condensed mb-3"><a href="https://services.github.com"
              data-ga-click="Footer, go to services, text:services" class="link-gray">Professional Services</a></li>
          <li class="lh-condensed mb-3"><a href="https://skills.github.com"
              data-ga-click="Footer, go to skills, text:skills" class="link-gray">Skills</a></li>
          <li class="lh-condensed mb-3"><a href="https://support.github.com?tags=dotcom-footer"
              data-ga-click="Footer, go to support, text:support" class="link-gray">Contact GitHub</a></li>
        </ul>
      </nav>

      <nav class="col-6 col-sm-3 col-lg-2 mb-6 mb-md-2 pr-3 pr-md-0 pl-md-4" aria-labelledby="footer-title-company">
        <h3 class="h5 mb-3 text-mono color-fg-muted text-normal" id="footer-title-company">Company</h3>
        <ul class="list-style-none f5">
          <li class="lh-condensed mb-3"><a href="https://github.com/about/"
              data-ga-click="Footer, go to support, text:support" class="link-gray">About</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/customer-stories?type=enterprise"
              data-ga-click="Footer, go to customer-stories, text:customer-stories" class="link-gray">Customer
              stories</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.blog/" data-ga-click="Footer, go to blog, text:blog"
              class="link-gray">Blog</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/readme"
              data-ga-click="Footer, go to readme, text:readme" class="link-gray">The ReadME Project</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.careers/"
              data-ga-click="Footer, go to careers, text:careers" class="link-gray">Careers</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/newsroom"
              data-ga-click="Footer, go to newsroom, text:newsroom" class="link-gray">Newsroom</a></li>
          <li class="lh-condensed mb-3"><a href="https://github.com/about/diversity"
              data-ga-click="Footer, go to diversity, text:diversity" class="link-gray">Inclusion</a></li>
          <li class="lh-condensed mb-3"><a href="https://socialimpact.github.com/"
              data-ga-click="Footer, go to socialimpact, text:socialimpact" class="link-gray">Social Impact</a></li>
          <li class="lh-condensed mb-3"><a href="https://shop.github.com/" data-ga-click="Footer, go to shop, text:shop"
              class="link-gray">Shop</a></li>
        </ul>
      </nav>
    </div>
  </div>

  <div class="color-bg-subtle">
    <div class="container-lg p-responsive f6 py-4 d-md-flex flex-justify-between flex-items-center">
      <nav aria-label="Legal and Resource Links">
        <ul class="list-style-none d-flex flex-wrap text-gray">
          <li class="mr-3">&copy;
            <script>document.write(new Date().getFullYear());</script> GitHub, Inc.
          </li>
          <li class="mr-3"><a href="https://docs.github.com/site-policy/github-terms/github-terms-of-service/"
              data-ga-click="Footer, go to terms, text:terms" class="link-gray">Terms</a></li>
          <li class="mr-3"><a href="https://help.github.com/articles/github-privacy-statement/"
              data-ga-click="Footer, go to privacy, text:privacy" class="link-gray">Privacy</a> (<a
              href="https://github.com/github/site-policy/pull/582" class="link-gray">Updated <time
                datetime="2022-08">08/2022</time></a>)</li>
        </ul>
      </nav>

      <nav aria-label="GitHub's Social Media Links" class="mt-3 mt-md-0">
        <ul class="list-style-none d-flex flex-wrap">
          <li class="mr-3"><a href="https://x.com/github" data-ga-click="Footer, go to Twitter, text:twitter"
              aria-label="GitHub X" style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>GitHub X</title>
                <path fill="currentColor"
                  d="M14.28 10.38L23.2 0h-2.1L13.8 9.02L7.14 0H0l10.13 14.7L0 25.5h2.1l7.64-9.38l6.9 9.38H23.2L12.72 10.38zM3.06 1.62h2.76L20.94 23.9h-2.76L3.06 1.62z" />
              </svg>
            </a></li>
          <li class="mr-3"><a href="https://www.facebook.com/GitHub"
              data-ga-click="Footer, go to Facebook, text:facebook" aria-label="GitHub Facebook"
              style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>GitHub Facebook</title>
                <path fill="currentColor"
                  d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
            </a></li>
          <li class="mr-3"><a href="https://www.linkedin.com/company/github"
              data-ga-click="Footer, go to Linkedin, text:linkedin" aria-label="GitHub LinkedIn"
              style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>GitHub LinkedIn</title>
                <path fill="currentColor"
                  d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
              </svg>
            </a></li>
          <li class="mr-3"><a href="https://www.youtube.com/github" data-ga-click="Footer, go to YouTube, text:youtube"
              aria-label="GitHub YouTube" style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>GitHub YouTube</title>
                <path fill="currentColor"
                  d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
              </svg>
            </a></li>
          <li class="mr-3"><a href="https://www.twitch.tv/github" data-ga-click="Footer, go to Twitch, text:twitch"
              aria-label="Twitch" style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>Twitch</title>
                <path fill="currentColor"
                  d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714z" />
              </svg>
            </a></li>
          <li class="mr-3"><a href="https://www.tiktok.com/@github" data-ga-click="Footer, go to TikTok, text:tiktok"
              aria-label="TikTok" style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>TikTok</title>
                <path fill="currentColor"
                  d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z" />
              </svg>
            </a></li>
          <li class="mr-3"><a href="https://github.com/github" data-ga-click="Footer, go to github's org, text:github"
              aria-label="GitHub.com" style="color: #959da5;">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="d-block" height="20" width="20"
                role="img">
                <title>GitHub.com</title>
                <path fill="currentColor"
                  d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
              </svg>
            </a></li>
        </ul>
      </nav>
    </div>
  </div>
</div>

<script>
  $('.components-container').toggleClass('one-column').toggleClass('two-columns')
  $(document).ready(function () {
    if ($('body').hasClass('status-none')) {
      $('link[rel="shortcut icon"]').attr("href", "https://github.githubassets.com/favicons/favicon-success.png")
    } else {
      $('link[rel="shortcut icon"]').attr("href", "https://github.githubassets.com/favicons/favicon-pending.png")
    }

    // Move "about this page" text section after the Incident History link
    var $statusParagraph = $('div.text-section > p').detach();
    // NOTE: We lookup last of this class for cases where there are multiple of them. We do not
    // want to insert the text muliple times on the page. For ex. when you have the 90 day history
    // enabled for components.
    $statusParagraph.insertAfter($('.history-footer-link').last());
    $('div.text-section').hide(); // hide the now-empty "About This Site" section

    // Hide the "Visit www.githubstatus.com..." component from the grid
    $('span.name:contains("Visit www.githubstatus.com")').closest('.component-container').hide();

    $('div.status-green span.component-status').html("")
    $('div.status-yellow span.component-status').html("")
    $('div.status-orange span.component-status').html("")
    $('div.status-red span.component-status').html("")
    $('.outage-field .label .major_outage').parent().html("Incident")

    var otherParent = $('span.name:contains("Other")').parent()
    if (otherParent.hasClass('status-green')) {
      otherParent.parent().hide()
    }
    $('.page-status.status-major span.status, .page-status.status-minor span.status').html('Some services are degraded')
    $('.outage-field .label .partial_outage').parent().html("Degradation")

    $('.incidents-list').remove()
    $('.component-statuses-legend').remove()

    $('div.status-green').append("<span class='status-msg'>Normal</span>")
    $('div.status-yellow').append("<span class='status-msg'>Degraded</span>")
    $('div.status-orange').append("<span class='status-msg'>Degraded</span>")
    $('div.status-red').append("<span class='status-msg'>Incident</span>")
    $('div.status-blue').append("<span class='status-msg'>Maintenance</span>")
  });
</script>
  </div>



      <script>
  /** INITIALIZATION **/
  var recaptchaIds = {}

  // Unfortunately there's no unique selectors on the parent divs that recaptcha adds. The first unique selector
  // is the iframe rendered 2 levels deep. So this waits until the iframes are added to the page, then finds
  // the parent div and sets the z index so that it'll render above our modals & dropdowns from the start.
  function setZIndex(captchaCount, startTime) {
    // bail after 10s just in case so we don't do this forever if something whaky happens
    if (new Date() - startTime > 10000) {
      return;
    }

    var iframes = document.querySelectorAll('iframe[title="recaptcha challenge"]');
    if (iframes.length != captchaCount) {
      setTimeout(function() {
        setZIndex(captchaCount, startTime);
      }, 500);
    }

    for (var i = 0; i < iframes.length; i++) {
      // incident subscribe modal is 1050, so this has to be above that
      iframes[i].parentElement.parentElement.style.zIndex = "1100";
    }
  }

  function updateCaptchaIframeTitle(captchaCount, startTime, updates=0) {

    if (new Date() - startTime > 10000 || captchaCount === updates) {
      return;
    }
    var iframesWithTitle = document.querySelectorAll('iframe[title="recaptcha challenge expires in two minutes"]');

    if (iframesWithTitle.length != captchaCount) {
      setTimeout(function() {
        updateCaptchaIframeTitle(captchaCount, startTime, iframesWithTitle.length + updates);
      }, 500);
    }

    for (var i = 0; i < iframesWithTitle.length; i++) {
      iframesWithTitle[i].title = "recaptcha";
    }
  }

  function addIncidentCaptcha() {
    var incidentCaptcha = document.createElement('div');
    incidentCaptcha.setAttribute('id', 'subscribe-incident-recaptcha');
    incidentCaptcha.setAttribute('class', 'g-recaptcha');
    incidentCaptcha.setAttribute('data-sitekey', '6LcZ-b0UAAAAAENi956aWzynTT2ZJ80dGU3F80Op');
    incidentCaptcha.setAttribute('data-callback', 'submitIncidentSubscriberSuccess');
    incidentCaptcha.setAttribute('data-error-callback', 'submitIncidentSubscriberError');
    incidentCaptcha.setAttribute('data-size', 'invisible');
    document.body.appendChild(incidentCaptcha);
    var incidentCode = document.createElement('input');
    incidentCode.setAttribute('type', 'hidden');
    incidentCode.setAttribute('id', 'submit_incident_code');
    document.body.appendChild(incidentCode);
  }

  var onloadCallback = function() {
    // if there is an incident, then add incident captcha element
    if (document.getElementsByClassName('modal-open-incident-subscribe').length > 0) {
      addIncidentCaptcha();
    }

    var captchas = document.getElementsByClassName("g-recaptcha");

    for(var i = 0; i < captchas.length; i++) {
      var elId = captchas[i].id;
      recaptchaIds[elId] = grecaptcha.enterprise.render(elId);
    }

    setZIndex(captchas.length, new Date());
    updateCaptchaIframeTitle(captchas.length, new Date());
  }


  /** SUBSCRIBE DROPDOWN */

  // callbacks for captcha success
  function submitNewSubscriber(type, error) {
    if (error) document.querySelector('#subscribe-form-' + type + ' #captcha_error').value = 'true';

    document.getElementById('subscribe-form-' + type).dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}));
    grecaptcha.enterprise.reset(recaptchaIds['subscribe-btn-' + type]);
  }
  function submitNewEmailSubscriber(token) {
    submitNewSubscriber('email');
  }
  function submitNewSmsSubscriber(token) {
    submitNewSubscriber('sms');
  }
  function submitNewWebhookSubscriber(token) {
    submitNewSubscriber('webhook');
  }
  function submitIncidentSubscriber(token, error) {
    var incidentCode = document.getElementById('submit_incident_code').value;
    var incidentForm = document.getElementById('subscribe-form-' + incidentCode);

    incidentForm.querySelector('input[name="captcha_error"]').value = error;
    incidentForm.querySelector('input[name="g-recaptcha-response"]').value = token;
    incidentForm.dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}));
    grecaptcha.enterprise.reset(recaptchaIds['subscribe-incident-recaptcha']);
  }
  function submitIncidentSubscriberSuccess(token) {
    submitIncidentSubscriber(token, 'false');
  }

  // callbacks if we get captcha network errors
  function emailSubscriberCaptchaError(token) {
    submitNewSubscriber('email', true);
  }
  function smsSubscriberCaptchaError(token) {
    submitNewSubscriber('sms', true);
  }
  function webhookSubscriberCaptchaError(token) {
    submitNewSubscriber('webhook', true);
  }
  function submitIncidentSubscriberError(token) {
    submitIncidentSubscriber(token, 'true');
  }

  // tracking clicks
  ['email', 'sms', 'webhook'].forEach(function(type) {
    var el = document.getElementById('subscribe-btn-' + type);
    el && el.addEventListener("click", function() {
      $.ajax({
        type: "POST",
        url: "/subscriptions/track_attempt",
        data: {
          type: type
        }
      })
    })
  })

  // form submission success callbacks
  $('#subscribe-form-email').on('ajax:success', function(e, data, status, xhr){
    if (data.type === 'success') {
      SP.currentPage.updatesDropdown.hide();
      var emailField = document.getElementById('email');
      if (emailField) {
        emailField.value = '';
      }
    }
  });
  $('#subscribe-form-sms').on('ajax:success', function(e, data, status, xhr){
    if (data.type === 'success' && data.otp_flow !== true) {
      SP.currentPage.updatesDropdown.hide();
      var phoneField = document.getElementById('phone-number');
      if (phoneField) {
        phoneField.value = '';
      }
    }
  });
  $('#subscribe-form-webhook').on('ajax:success', function(e, data, status, xhr){
    if (data.type === 'success') {
      SP.currentPage.updatesDropdown.hide();
      document.getElementById('endpoint-webhooks').value = '';
      document.getElementById('email-webhooks').value = '';
    }
  });

  $('a.subscribe').on('click', function() {
    document.body.style.overflow = "hidden";
    document.body.style.height = "100vh";
  });

  $('div.modal-open-incident-subscribe').on('hidden', function(){
    document.body.style.overflow = "";
    document.body.style.height = "";
  });

  function submitCaptchaIncidentSubscribe(event) {
    var incidentCode = event.target.id.split('-')[2];
    event.preventDefault();

    $.ajax({
      type: "POST",
      url: "/subscriptions/track_attempt",
      data: {
        type: 'incident'
      }
    })

    document.getElementById('submit_incident_code').value = incidentCode;
    grecaptcha.enterprise.execute(recaptchaIds['subscribe-incident-recaptcha']);
  }
</script>

<script src='https://www.recaptcha.net/recaptcha/enterprise.js?onload=onloadCallback&render=explicit' async defer></script>


    
  <script src="https://dka575ofm4ao0.cloudfront.net/packs/common-22300aadeedc33be4ddc.chunk.js"></script>
  <script src="https://dka575ofm4ao0.cloudfront.net/packs/globals-f12471d5e878ec0f0705.chunk.js"></script>

    <script src="https://dka575ofm4ao0.cloudfront.net/packs/runtime-33399279767e29d9b814.js"></script>
    
    
    <script src="https://dka575ofm4ao0.cloudfront.net/packs/status-6ff5e210aa5463ca1499.chunk.js"></script>
    <script src="https://dka575ofm4ao0.cloudfront.net/packs/components-fd678426d9b004eeecc7.chunk.js"></script>


    <script>
  window.addEventListener('load', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const messageToken = urlParams.get('slack_message_token');
    const channelName = escape(urlParams.get('channel_name'));

    if(!!messageToken) {
      switch(messageToken) {
        case 'slack_auth_error':
          HRB.utils.notify('The Slack authorization attempt was unsuccessful. Try again.', {cssClass:'error'});
          break;
        case 'subscribers_disabled_error':
          HRB.utils.notify('Slack subscriptions are not enabled on this page.', {cssClass:'error'});
          break;
        case 'direct_message_channel_error':
          HRB.utils.notify('Subscriptions aren’t supported in direct messages. Try subscribing again and choose a channel instead.', {cssClass:'error'});
          break
        case 'duplicate_error':
          HRB.utils.notify("You're already subscribed to get Slack notifications in that channel.", {cssClass:'error'});
          break;
        case 'duplicate_private_channel_error':
          HRB.utils.notify(`You're already subscribed to get Slack notifications in #${channelName}. Invite the @Statuspage app to that channel to start getting status updates.`, {cssClass: 'error'});
          break;
        case 'default_success':
          HRB.utils.notify("You're now subscribed to get Statuspage updates in Slack!", {cssClass:'success'});
          break;
        case 'private_channel_success':
          HRB.utils.notify(`IMPORTANT: Invite the @Statuspage app to your Slack channel #${channelName} to start getting status updates.`, {cssClass:'success'});
          break;
      }
    }
  });
</script>

    
<!-- FOR FLASH NOTICES -->

<!-- FOR ERROR -->


    <script>
  $(function() {
    var $link = $('<span class="color-secondary powered-by"><a class="color-secondary" target="_blank" rel="noopener noreferrer nofollow" href="https://www.atlassian.com/software/statuspage?utm_campaign=www.githubstatus.com&amp;utm_content=SP-notifications&amp;utm_medium=powered-by&amp;utm_source=inapp">Powered by Atlassian Statuspage</a></span>');

  	var setPoweredByStyles = function() {
  		if (!$('.powered-by').length) {
  			$link.appendTo($('.page-footer'))
  		}
  		$('.powered-by').attr('style', 'display: inline !important; visibility:visible !important; opacity: 1 !important; position:static !important; text-indent:0px !important; transform:scale(1) !important');
  	}

  	setInterval(setPoweredByStyles, 1000);
  });
</script>





  </body>
</html>
