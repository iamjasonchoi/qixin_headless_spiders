<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml" encoding="UTF-8" indent="yes" />
    <xsl:template match="/">
        <list>
			<xsl:for-each select="//div[contains(@class, 'company-item')]">
                <item>
                    <title>
                        <xsl:value-of select=".//div[@class='company-title']/a/text()"/>
                    </title>
                    <legal_owner>
                        <xsl:value-of select=".//div[@class='legal-person'][1]/text()"/>
                    </legal_owner>
                    <status>
                        <xsl:value-of select=".//div[@class='company-tags']/span[1]/text()"/>
                    </status>
                    <capital>
                        <xsl:value-of select=".//div[contains(@class, 'col-3-1')]/text()"/>
                    </capital>
                    <date>
                        <xsl:value-of select=".//div[contains(@class, 'col-3-2')]/text()"/>
                    </date>
                    <url>
                       <xsl:value-of select=".//div[@class='company-title']/a/@href"/>
				   </url>
                </item>
            </xsl:for-each>
        </list>
    </xsl:template>
</xsl:stylesheet>
