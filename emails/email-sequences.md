<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="description" content="Bounty Alert Blitz – New Opportunity">
  <title>Bounty Alert Blitz – New Opportunity</title>
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <style>
    table {border-collapse:collapse;}
    td {border-collapse:collapse;}
    .mso-hide {display:none;}
  </style>
  <![endif]-->
  <!--[if !mso]><!-->
  <style>
    .mso-hide {display:none;}
  </style>
  <!--<![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">
  <!--[if mso]>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4;" border="0">
    <tr>
      <td align="center" valign="top" style="padding: 20px 10px;">
  <![endif]-->

  <!-- Outer wrapper: full-bleed background + centering -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; mso-line-height-rule: exactly;">
    <tr>
      <td align="center" style="padding: 20px 10px;">
        <!--[if mso]>
        <table role="presentation" width="600" align="center" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="padding: 0;">
        <![endif]-->

        <!-- Main content table: max-width 600px, white bg, rounded corners, shadow -->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.15); mso-line-height-rule: exactly;">
          <tr>
            <td style="padding: 0;">
              <!-- ==================== HEADER (role="banner") ==================== -->
              <!--
                SERVER-SIDE LOGGING:
                  INFO: Starting render for recipient {email}.
                  DEBUG: Dynamic header content loaded for bounty {id} -> {headingText}.
                  WARN: headingText empty after validation – using default fallback.
                  ERROR: Header rendering failed: {exception} – send plain text fallback.
              -->
              <div role="banner" style="padding: 40px 30px 20px;">
                <!--
                  PLACEHOLDER: headingText
                  @type {string} headingText – heading for the email
                  VALIDATION: HTML-escape all dynamic content (e.g. & → &amp;). Strip disallowed tags.
                  FALLBACK: "🚀 Bounty Alert Blitz"
                  EXAMPLE: server-side: {{ sanitizeHeadline(headingText) }}
                -->
                <h1 style="margin: 0 0 20px 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 28px; color: #1a73e8; text-align: center; line-height: 1.3;">
                  🚀 Bounty Alert Blitz
                </h1>
              </div>

              <!-- ==================== BODY (role="main") ==================== -->
              <div role="main" style="padding: 0 30px 20px;">
                <!--
                  PLACEHOLDER: description
                  @type {string} description – HTML body text (limited tags: b, i, a, p, br)
                  VALIDATION:
                    - Allow only whitelisted HTML tags: <b>, <i>, <a>, <p>, <br>.
                    - Allowed attributes: href (must be https), target, rel.
                    - Strip all other tags and attributes.
                    - Encode HTML entities in text content.
                  FALLBACK: "A new bounty opportunity is available. Check the link below for details."
                  LOGGING:
                    DEBUG: Description loaded with length {len}.
                    WARN: Description contained disallowed tags – sanitized.
                -->
                <p style="margin: 0 0 20px 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; color: #333333; line-height: 1.6;">
                  A new bounty opportunity is available. Check the link below for details.
                </p>

                <!--
                  PLACEHOLDER: rewardDetails
                  @type {string} rewardDetails – reward amount or description
                  VALIDATION: Same as description (limited HTML).
                  FALLBACK: "5000 MRG"
                -->
                <p style="margin: 0 0 20px 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; color: #333333; line-height: 1.6;">
                  <strong>Reward:</strong> 5000 MRG
                </p>

                <!--
                  PLACEHOLDER: deadlineText
                  @type {string} deadlineText – deadline date/time
                  VALIDATION: Plain text, HTML-escaped.
                  FALLBACK: "No deadline specified"
                -->
                <p style="margin: 0 0 20px 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; color: #333333; line-height: 1.6;">
                  <strong>Deadline:</strong> 2026-06-15 23:59 UTC
                </p>

                <!--
                  PLACEHOLDER: ctaUrl, ctaText
                  @type {string} ctaUrl – validated HTTPS URL (no HTTP, no javascript:)
                  @type {string} ctaText – button label, plain text
                  VALIDATION:
                    - ctaUrl: must start with https://, no path traversal, no script injection.
                      Use URL parsing and validation library, reject invalid.
                      Fallback: replace with support page URL (e.g. https://support.example.com/bounties).
                    - ctaText: HTML-escaped.
                  LOGGING:
                    DEBUG: CTA URL validated OK.
                    WARN: CTA URL validation failed – using fallback.
                    ERROR: CTA rendering error – skip button.
                -->
                <!--[if mso]>
                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{{ ctaUrl | url_fallback }}" style="height:44px;v-text-anchor:middle;width:220px;" arcsize="18%" stroke="f" fillcolor="#1a73e8">
                  <w:anchorlock/>
                  <center style="color:#ffffff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:16px;font-weight:bold;">{{ ctaText | sanitize }}</center>
                </v:roundrect>
                <![endif]-->
                <!--[if !mso]><!-->
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto 20px auto;">
                  <tr>
                    <td align="center" style="background-color: #1a73e8; border-radius: 8px; padding: 12px 30px; mso-hide: all;">
                      <a href="{{ ctaUrl | url_validate }}" target="_blank" rel="noopener noreferrer" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; color: #ffffff; text-decoration: none; font-weight: bold; display: block;" aria-label="{{ ctaText | sanitize }} – opens in new tab">
                        {{ ctaText | sanitize }}
                      </a>
                    </td>
                  </tr>
                </table>
                <!--<![endif]-->
              </div>

              <!-- ==================== FOOTER (role="contentinfo") ==================== -->
              <!--
                LOGGING:
                  INFO: Footer rendering started.
                  DEBUG: Unsubscribe link prepared.
                  ERROR: Footer rendering failed – skip block.
              -->
              <div role="contentinfo" style="padding: 20px 30px; background-color: #f9f9f9; border-top: 1px solid #eeeeee; border-radius: 0 0 8px 8px;">
                <p style="margin: 0 0 10px 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 12px; color: #666666; text-align: center; line-height: 1.5;">
                  You received this because you subscribed to bounty alerts.
                  <br>
                  <!--
                    PLACEHOLDER: unsubscribeUrl
                    @type {string} unsubscribeUrl – HTTPS URL or mailto with predefined subject
                    VALIDATION:
                      - If URL: must be HTTPS, no injection.
                      - If mailto: must be valid RFC 5322, no extra headers.
                    FALLBACK: no unsubscribe link (but include placeholder text)
                    LOGGING:
                      DEBUG: Unsubscribe link initialized.
                      WARN: Unsubscribe URL validation failed – omitted.
                  -->
                  <a href="{{ unsubscribeUrl | url_validate }}" target="_blank" rel="noopener noreferrer" style="color: #1a73e8; text-decoration: underline;">Unsubscribe</a>
                  <br>
                  &copy; 2026 Bounty Blitz, Inc. All rights reserved.
                </p>
              </div>
            </td>
          </tr>
        </table>

        <!--[if mso]>
            </td>
          </tr>
        </table>
        <![endif]-->
      </td>
    </tr>
  </table>

  <!--[if mso]>
      </td>
    </tr>
  </table>
  <![endif]-->

  <!--
    ============================================================================
    SERVER-SIDE ERROR HANDLING (pseudo-code)
    try {
        // Load dynamic content from database/API
        $data = loadBountyData($bountyId);
        if (!$data) {
            throw new Exception("No bounty data found for ID $bountyId");
        }
        // Validate and sanitize all fields
        $heading = sanitizeString($data['heading'], 100);
        $description = sanitizeHtml($data['description']);
        $ctaUrl = validateUrl($data['ctaUrl'], 'https://support.example.com/bounties');
        // ... other fields
        // Render template with escaped data
        renderEmailTemplate($heading, $description, $ctaUrl, ...);
    } catch (Exception $e) {
        // Log full error
        Logger::error("Email rendering failed", ['bountyId' => $bountyId, 'error' => $e->getMessage()]);
        // Send plain-text fallback or skip
        sendPlainTextFallback($recipient);
    }
    ============================================================================
  -->

  <!--
    ADDITIONAL EMAIL HEADERS (set by server-side sending layer):
    - List-Unsubscribe: <mailto:unsubscribe@example.com?subject=unsubscribe>
    - Content-Security-Policy: default-src 'none'; img-src https:;
    - X-Mailer: BountyBlitz/3.0
    - Precedence: bulk
  -->
</body>
</html>