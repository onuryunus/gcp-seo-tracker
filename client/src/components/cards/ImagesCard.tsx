import React, { useState } from 'react';
import { Image, Eye, EyeOff, Tag } from 'lucide-react';
import { ImageAnalysisResult } from '../../types';

interface ImagesCardProps {
  images: ImageAnalysisResult[];
  className?: string;
}

const ImagesCard: React.FC<ImagesCardProps> = ({
  images,
  className = ''
}) => {
  const [expandedImage, setExpandedImage] = useState<number | null>(null);
  const [showImages, setShowImages] = useState(true);

  const imagesWithIssues = images.filter(img => !img.alt_text || img.alt_text.trim() === '');
  const imagesWithAltText = images.filter(img => img.alt_text && img.alt_text.trim() !== '');

  return (
    <div className={`bg-white rounded-lg border border-gray-200 overflow-hidden ${className}`}>
      <div className="px-6 py-4 bg-purple-50 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-purple-700 flex items-center gap-2">
              <Image className="w-5 h-5" />
              Image Analysis
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {images.length} images analyzed • {imagesWithIssues.length} missing alt text
            </p>
          </div>
          <button
            onClick={() => setShowImages(!showImages)}
            className="flex items-center gap-2 px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {showImages ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            {showImages ? 'Hide Images' : 'Show Images'}
          </button>
        </div>
      </div>

      <div className="p-6">
        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{images.length}</div>
            <div className="text-sm text-gray-600">Total Images</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{imagesWithAltText.length}</div>
            <div className="text-sm text-gray-600">With Alt Text</div>
          </div>
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">{imagesWithIssues.length}</div>
            <div className="text-sm text-gray-600">Missing Alt Text</div>
          </div>
        </div>

        {/* Images List */}
        {images.length === 0 ? (
          <div className="text-center py-8">
            <Image className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No images found on this page</p>
          </div>
        ) : (
          <div className="space-y-4">
            {images.map((image, index) => (
              <div
                key={index}
                className={`border rounded-lg p-4 ${
                  !image.alt_text || image.alt_text.trim() === ''
                    ? 'border-red-200 bg-red-50'
                    : 'border-green-200 bg-green-50'
                }`}
              >
                <div className="flex items-start gap-4">
                  {/* Image Preview */}
                  {showImages && (
                    <div className="flex-shrink-0">
                      <img
                        src={image.image_link}
                        alt={image.alt_text || 'No alt text'}
                        className="w-16 h-16 object-cover rounded-lg border border-gray-200"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.style.display = 'none';
                        }}
                      />
                    </div>
                  )}

                  <div className="flex-1 min-w-0">
                    {/* Image URL */}
                    <div className="mb-3">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {image.image_link}
                      </p>
                    </div>

                    {/* Alt Text Status */}
                    <div className="mb-3">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-medium text-gray-700">Current Alt Text:</span>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          image.alt_text && image.alt_text.trim() !== ''
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {image.alt_text && image.alt_text.trim() !== '' ? 'Present' : 'Missing'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 bg-white p-2 rounded border">
                        {image.alt_text || 'No alt text provided'}
                      </p>
                    </div>

                    {/* Suggested Alt Text */}
                    {image.alt_text_suggestion && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-gray-700 mb-1">Suggested Alt Text:</p>
                        <p className="text-sm text-blue-700 bg-blue-50 p-2 rounded border border-blue-200">
                          {image.alt_text_suggestion}
                        </p>
                      </div>
                    )}

                    {/* Keywords */}
                    {image.keywords && image.keywords.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-1">
                          <Tag className="w-4 h-4" />
                          Related Keywords:
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {image.keywords.map((keyword, keywordIndex) => (
                            <span
                              key={keywordIndex}
                              className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full"
                            >
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Expand/Collapse Button */}
                  <button
                    onClick={() => setExpandedImage(expandedImage === index ? null : index)}
                    className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-600"
                  >
                    {expandedImage === index ? '−' : '+'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ImagesCard;
