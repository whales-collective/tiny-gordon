package main

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"

	containertypes "github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/image"
	"github.com/docker/docker/client"
)

func main() {
	// Create MCP server
	s := server.NewMCPServer(
		"talk-to-moby",
		"0.0.0",
	)

	// Add a tool
	mobyRunningContainers := mcp.NewTool("display_running_containers",
		mcp.WithDescription("use docker to display the list of running containers on the host"),
	)
	mobyRunningAllContainers := mcp.NewTool("display_running_all_containers",
		mcp.WithDescription("use docker to display the list of all containers on the host"),
	)

	mobyListAllImages := mcp.NewTool("display_list_all_images",
		mcp.WithDescription("use docker to display the list of all images on the host"),
	)

	// Add a tool handler
	s.AddTool(mobyRunningContainers, mobyRunningContainersHandler)
	s.AddTool(mobyRunningAllContainers, mobyRunningAllContainersHandler)
	s.AddTool(mobyListAllImages, mobyListAllImagesHandler)

	// Start the stdio server
	if err := server.ServeStdio(s); err != nil {
		fmt.Printf("❌ Failed to start server: %v\n", err)
		return
	}
}

func mobyRunningContainersHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {

	//ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}
	defer cli.Close()

	containers, err := cli.ContainerList(ctx, containertypes.ListOptions{})
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}

	content := ""
	for _, container := range containers {
		content += fmt.Sprintf("ID: %s, Names: %v, Status: %s\n", container.ID, container.Names, container.Status)
	}

	return mcp.NewToolResultText(content), nil
}

func mobyRunningAllContainersHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}
	defer cli.Close()

	// Ajout de All: true pour lister tous les conteneurs (y compris arrêtés)
	containers, err := cli.ContainerList(ctx, containertypes.ListOptions{All: true})
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}

	content := ""
	for _, container := range containers {
		content += fmt.Sprintf("ID: %s, Names: %v, Status: %s\n", container.ID, container.Names, container.Status)
	}

	return mcp.NewToolResultText(content), nil
}

func mobyListAllImagesHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {

	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}
	defer cli.Close()

	images, err := cli.ImageList(ctx, image.ListOptions{})
	if err != nil {
		panic(err)
	}

	content := ""
	for _, image := range images {
		content += fmt.Sprintf("ID: %s, RepoTags: %v, Size: %d bytes\n", image.ID, image.RepoTags, image.Size)
	}

	return mcp.NewToolResultText(content), nil
}
