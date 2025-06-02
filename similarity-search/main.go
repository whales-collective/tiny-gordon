package main

import (
	"context"
	"encoding/binary"
	"fmt"
	"math"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"

	"github.com/redis/go-redis/v9"
)

// MODEL_RUNNER_BASE_URL=http://localhost:12434 go run main.go
func main() {

	// Create MCP server
	s := server.NewMCPServer(
		"docker-search",
		"0.0.0",
	)

	// Add a tool
	searchInDoc := mcp.NewTool("docker_command",
		mcp.WithDescription(`Perform a similarity search between the user question and the documents in the knowledge base. 
		The knowledge base is created from the documents.
		`),
		mcp.WithString("question",
			mcp.Required(),
			mcp.Description("Search question"),
		),
	)
	s.AddTool(searchInDoc, searchInDocHandler)

	// Start the stdio server
	if err := server.ServeStdio(s); err != nil {
		fmt.Printf("❌ Failed to start server: %v\n", err)
		return
	}

}

func searchInDocHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {

	args := request.GetArguments()
	question := args["question"].(string)

	// Docker Model Runner Chat base URL
	//llmURL := os.Getenv("DMR_BASE_URL") + "/engines/llama.cpp/v1/"
	llmURL := "http://model-runner.docker.internal/engines/llama.cpp/v1/"
	//embeddingsModel := os.Getenv("MODEL_RUNNER_EMBEDDING_MODEL")
	embeddingsModel := "ai/mxbai-embed-large:latest"

	client := openai.NewClient(
		option.WithBaseURL(llmURL),
		option.WithAPIKey(""),
	)

	// EMBEDDINGS...
	// -------------------------------------------------
	// Generate embeddings from chunks
	// -------------------------------------------------
	rdb, err := InitializeRedis(ctx)
	if err != nil {
		return mcp.NewToolResultError("🔴🔴🔴: " + err.Error()), nil
	}

	// USER QUESTION:
	userQuestion := question

	// -------------------------------------------------
	// Generate embeddings from user question
	// -------------------------------------------------
	// EMBEDDINGS...
	//fmt.Println("⏳ Creating embeddings from user question...")

	embeddingsFromUserQuestion, err := client.Embeddings.New(ctx, openai.EmbeddingNewParams{
		Input: openai.EmbeddingNewParamsInputUnion{
			OfString: openai.String(userQuestion),
		},
		Model: embeddingsModel,
	})

	if err != nil {
		return mcp.NewToolResultError("🔴: " + err.Error()), nil
	}

	//fmt.Println("✋ embeddings from the user question:\n", embeddingsFromUserQuestion.Data[0].Embedding)

	// convert the embedding to a []float32
	embedding := make([]float32, len(embeddingsFromUserQuestion.Data[0].Embedding))
	for i, f := range embeddingsFromUserQuestion.Data[0].Embedding {
		embedding[i] = float32(f)
	}

	buffer := floatsToBytes(embedding)

	// SIMILARITY SEARCH:
	// Search for similar documents in Redis
	//fmt.Println("⏳ Searching for similar documents in Redis...")
	results, err := rdb.FTSearchWithArgs(ctx,
		"vector_idx",
		"*=>[KNN 5 @embedding $vec AS vector_distance]",
		&redis.FTSearchOptions{
			Return: []redis.FTSearchReturn{
				{FieldName: "vector_distance"},
				{FieldName: "content"},
			},
			DialectVersion: 2,
			Params: map[string]any{
				"vec": buffer,
			},
		},
	).Result()

	if err != nil {
		return mcp.NewToolResultError("🟢: " + err.Error()), nil
	}

	//fmt.Println("🎉 Found", len(results.Docs), "similarities")

	knowledgeBase := ""
	// CONTEXT: create context from the similarities
	for _, doc := range results.Docs {
		//fmt.Println("📝 ID:", doc.ID, "Distance:", doc.Fields["vector_distance"])
		//fmt.Println("📝 Content:\n", doc.Fields["content"])
		knowledgeBase += doc.Fields["content"]
	}
	/*
		The results are ordered according to the value of the vector_distance field,
		with the lowest distance indicating the greatest similarity to the query.
	*/

	content := fmt.Sprintf("🎉 Found %d similarities. Query: %s. Content: %s", len(results.Docs), question, knowledgeBase)
	//fmt.Println("📝 Content:\n", content)

	return mcp.NewToolResultText(content), nil
}

func InitializeRedis(ctx context.Context) (*redis.Client, error) {
	// connect to Redis and delete any index previously created with the name vector_idx:
	rdb := redis.NewClient(&redis.Options{
		//Addr:     "redis-server:6379",
		//Addr:     "0.0.0.0:6379",
		Addr:     "host.docker.internal:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
		Protocol: 2,
	})

	return rdb, nil

}

func floatsToBytes(fs []float32) []byte {
	buf := make([]byte, len(fs)*4)

	for i, f := range fs {
		u := math.Float32bits(f)
		binary.NativeEndian.PutUint32(buf[i*4:], u)
	}

	return buf
}
