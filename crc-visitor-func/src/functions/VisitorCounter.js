module.exports = async (request, context) => {
  context.log("🚀 VisitorCounter function invoked");

  try {
    const { TableClient, AzureNamedKeyCredential } = require("@azure/data-tables");

    const account = process.env.TABLE_ACCOUNT;
    const accountKey = process.env.TABLE_KEY;
    const tableName = process.env.TABLE_NAME;

    const partitionKey = "resume";
    const rowKey = "visitorCounter";

    const credential = new AzureNamedKeyCredential(account, accountKey);
    const client = new TableClient(
      `https://${account}.table.cosmos.azure.com:443`,
      tableName,
      credential
    );

    let entity;

    try {
      context.log("📦 Attempting to fetch entity...");
      const fetched = await client.getEntity(partitionKey, rowKey);
      context.log("✅ Entity found:", fetched);

      // Strip out system properties
      const { count, ...rest } = fetched;
      entity = {
        partitionKey,
        rowKey,
        count: Number(count || 0) + 1
      };

      context.log("💾 Updating entity:", entity);
      await client.updateEntity(entity, "Replace");

    } catch (err) {
      context.log("⚠️ Entity fetch or update failed:", err.message);

      if (err.statusCode === 404) {
        context.log("🆕 Creating new entity.");
        entity = {
          partitionKey,
          rowKey,
          count: 1
        };
        await client.createEntity(entity);
      } else {
        throw err;
      }
    }

    return {
      status: 200,
      jsonBody: { count: entity.count }
    };
  } catch (error) {
    context.log("💥 Top-level error:", error.message);
    return {
      status: 500,
      body: "Internal Server Error"
    };
  }
};
