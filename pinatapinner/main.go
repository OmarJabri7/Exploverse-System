package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"

var (
	pinataAPIKey    string
	pinataSecretKey string
)

// Just like main, but supports "return <status_code>" to make things easier
func mainWithExitCode() int {
	// Check if the env vars are set
	pinataAPIKey = "3c783a682ddd6638e737"
	pinataSecretKey = "7193f4e2cc55bbd52c72b1313ba1dd7864fb848af159268227c461690508fa8d"
	if pinataAPIKey == "" || pinataSecretKey == "" {
		fmt.Println("Environmental variables `PINATA_API_KEY` and `PINATA_SECRET_KEY` are required")
		return 1
	}

	// Ensure that we have a folder to pin
	if len(os.Args) < 2 {
		fmt.Println("Need to specify the folder to pin")
		return 1
	}
	folder := os.Args[1]
	exists, err := folderExists(folder)
	if err != nil {
		fmt.Println("Error while reading filesystm:", err)
		return 2
	}
	if !exists {
		fmt.Println("Folder doesn't exist or isn't a folder")
		return 1
	}

	// Check if we have a name for the bundle
	name := "Pinned via Pinata Pinner"
	if len(os.Args) > 2 {
		name = os.Args[2]
	}

	// Pin the folder
	err = pinFolder(folder, name)
	if err != nil {
		fmt.Println("Error while pinning folder:", err)
		return 2
	}

	return 0
}

// type filePart struct {
// 	file      *os.File //File handler
// 	fileSize  int64    //File size
// 	baseName  string   //Base name (may differs from orignal base-name)
// 	filePath  string   //Original filename
// 	fieldName string   //Name of field in multipart content
// 	mpBegin   []byte   //Beginning of the multipart
// }

// type fieldPart struct {
// 	name   string //field name
// 	value  string //field value
// 	mpData []byte //multipart data
// }

// type FormUploader interface {
// 	AddField(name, value string) FormUploader
// 	AddFields(fields map[string]string) FormUploader
// 	Fields(name string) []string
// 	AddFiles(fieldName string, basePath string, files ...string) error
// 	Files() []string
// 	SetChunkSize(size int64) FormUploader
// 	ChunkSize() int64
// 	Post(client *http.Client, targetURL string, headers map[string]string) (*http.Response, error)
// 	Put(client *http.Client, targetURL string, headers map[string]string) (*http.Response, error)
// }

// type formUploader struct {
// 	chunkSize int64
// 	fields    []*fieldPart
// 	files     []*filePart
// 	*FormUploader
// }

// func NewFormUploader() FormUploader {
// 	return &formUploader{chunkSize: 1024 * 10}
// }

// Pins a folder
func pinFolder(folder string, name string) error {
	// Build the request
	fu := NewFormUploader()

	// Scan for files and add them
	files := make([]string, 0)
	err := filepath.Walk(folder,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			// Add files only
			if info.Mode().IsRegular() {
				// Remove the folder from the beginning of the file's name
				path = strings.TrimPrefix(path, folder)
				// Trim again an optional path separator
				path = strings.TrimPrefix(path, string(os.PathSeparator))
				files = append(files, path)
			}
			return nil
		})
	if err != nil {
		return err
	}
	fu.AddFiles("file", folder, files...)

	// Add the name
	keyValues := make(map[string]string)
	keyValues["PinnedBy"] = "https://github.com/ItalyPaleAle/pinatapinner"
	pinataMetadata := struct {
		Name      string            `json:"name"`
		KeyValues map[string]string `json:"keyvalues"`
	}{
		Name:      name,
		KeyValues: keyValues,
	}
	pinataMetadataJSON, err := json.Marshal(pinataMetadata)
	if err != nil {
		return err
	}
	fu.AddField("pinataMetadata", string(pinataMetadataJSON))

	// Send the request
	client := &http.Client{
		// Do not set a timeout, as the files might be large
		Timeout: 0,
	}
	headers := make(map[string]string, 2)
	headers["pinata_api_key"] = pinataAPIKey
	headers["pinata_secret_api_key"] = pinataSecretKey
	resp, err := fu.Post(client, endpoint, headers)
	if err != nil {
		return err
	}

	// Get the response
	res, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	// If status code isn't 2xx, we have an error
	if resp.StatusCode < 200 || resp.StatusCode > 299 {
		return fmt.Errorf("invalid response status code: %d", resp.StatusCode)
	}

	// Output the response (should be a JSON)
	fmt.Println(string(res))

	return nil
}

func folderExists(path string) (bool, error) {
	info, err := os.Stat(path)
	if err != nil {
		// Ignore the error if it's a "not exists", that's the goal
		if os.IsNotExist(err) {
			err = nil
		}
		return false, err
	}
	if info.IsDir() {
		// Exists and it's a folder
		return true, nil
	}
	// Exists, but not a folder
	return false, nil
}

// Entry point
func main() {
	os.Exit(mainWithExitCode())
}
