# Idea Box CLI
Capture and organize your ideas effortlessly from the command line.

## Features
- Capture ideas with customizable tags.
- List and search ideas by tags.
- Export your ideas to JSON format for easy sharing.

## Quickstart
To get started with Idea Box CLI, follow these simple steps:

1. **Install the CLI**:
   ```bash
   npm install -g idea-box-cli
   ```

2. **Run the CLI**:
   ```bash
   idea-box
   ```

## Usage Examples
- **Add a new idea**:
   ```bash
   idea-box add "Build a website" --tags web,portfolio
   ```

- **List all ideas**:
   ```bash
   idea-box list
   ```

- **Search ideas by tag**:
   ```bash
   idea-box search --tag web
   ```

- **Export ideas to JSON**:
   ```bash
   idea-box export --output ideas.json
   ```

## Configuration
Configuration settings can be adjusted in the `~/.idea-box/config.json` file. Key options include:
- `defaultTags`: Set default tags for new ideas.
- `exportPath`: Specify the default path for exported JSON files.

## Roadmap
- [ ] Implement idea prioritization feature.
- [ ] Add user authentication for syncing ideas across devices.
- [ ] Enhance search capabilities with advanced filtering.

## FAQ
**Q: Can I use Idea Box CLI without Node.js?**  
A: No, Node.js is required to run the CLI.

**Q: How do I uninstall the CLI?**  
A: You can uninstall it using:
```bash
npm uninstall -g idea-box-cli
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.