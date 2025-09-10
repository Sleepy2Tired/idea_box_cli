# Idea Box CLI
Capture and organize your ideas instantly from the command line.

## Features
- **Instant Idea Capture**: Quickly add ideas without distraction.
- **Categorization**: Organize ideas into customizable categories.
- **Search Functionality**: Easily find ideas by keywords or categories.
- **Export Options**: Save your ideas in various formats for easy sharing.
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux.

## Quickstart

### Installation
To install Idea Box CLI, run the following command:

```bash
npm install -g idea-box-cli
```

### Running the Tool
Once installed, you can start the CLI by executing:

```bash
idea-box
```

## Usage Examples

- **Add a New Idea**:
  ```bash
  idea add "Build a personal website" --category "Web Development"
  ```

- **List All Ideas**:
  ```bash
  idea list
  ```

- **Search Ideas by Keyword**:
  ```bash
  idea search "website"
  ```

- **Export Ideas**:
  ```bash
  idea export --format json
  ```

## Configuration
Customize your Idea Box CLI settings by creating a configuration file at `~/.idea-box/config.json`. Here’s an example configuration:

```json
{
  "defaultCategory": "General",
  "exportFormat": "txt"
}
```

## Roadmap
- [ ] Implement tagging system for ideas.
- [ ] Add reminder functionality for follow-up on ideas.
- [ ] Introduce collaborative features for team usage.
- [ ] Enhance export options with more formats.

## FAQ

**Q: Can I use Idea Box CLI without Node.js?**  
A: No, Node.js is required to run Idea Box CLI.

**Q: How can I contribute to the project?**  
A: Feel free to fork the repository and submit a pull request with your improvements.

**Q: Is there a mobile version available?**  
A: Currently, Idea Box CLI is only available as a command-line tool.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.