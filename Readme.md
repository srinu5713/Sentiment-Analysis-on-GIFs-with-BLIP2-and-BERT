# Sentiment Analysis Using GIFs with BLIP2 and BERT

This project implements sentiment analysis on GIFs by leveraging the BLIP2 model for caption generation and the BERT model for sentiment analysis. The approach involves splitting GIFs into multiple frames, generating captions for each frame, and ensemble analyzing the sentiments to get an accurate result. This method is more efficient than traditional single-frame analysis and can be used for applications such as social media analysis, understanding user comments, and interactions.

## Key Features

- **BLIP2 Model:** Generates captions for GIF frames.
- **BERT Model:** Performs sentiment analysis on the generated captions.
- **Ensemble Sentiment Analysis:** Combines emotions from multiple frames for accurate sentiment detection.

## File Structure


```plaintext
.
├── Blip2_model_lstm.ipynb # Training BLIP2 model using TGIF dataset
├── Sentiment_Analysis_using_Bert.ipynb # Training BERT model for sentiment analysis using Twitter dataset
├── sentiment_analysis_using_bert.py # Script for sentiment analysis using BERT
├── Sentiment_analysis_of_GIFs_using_BlIP2_and_BERT.ipynb # Combined file containing both models
├── tgif-v1.0.tsv # TGIF dataset
├── twitter_data.csv # Twitter sentiment dataset
├── LICENSE # License file
├── README.md # Readme file

```
## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to explore the code, experiment with different configurations, and contribute to the advancement of file management tools. For any questions or issues, please open an issue in the repository. Thank you for your interest and contributions!
