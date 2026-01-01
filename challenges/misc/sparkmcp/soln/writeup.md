# Solution

1.  Connect your LLM to the SparkMCP server using the provided [JSON file configuration](../dist/mcpserver.json).

2.  There is a tool called `get_flag` that outputs a fake flag.

    ![get_flag shown](mcp_config.png)
    ![get_flag output](get_flag_output.png)

3.  There is also another tool called `request_info` that includes the information `client_id`, showing that we are only a `guest` user.

    ![session_info](req_info.png)

3. Perform SQL Injection on the tool `get_tools` to obtain the tables that exist in the database.

    ![table_query](table_query.png)

4.  Do a separate SQL Injection payload to obtain the token.

    ![query_sql](query_sql.png)

5.  Now change the authentication token to make use of the `admin` token. From there restart the MCP client to save these changes.

    ![admin_token](admin_token.png)

6.  Make use of the `get_flag` tool again to finally get the real flag.

    ![flag](flag.png)
