package org.opencv.samples.facedetect;

import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfDouble;
import org.opencv.imgproc.Imgproc;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.text.Html;

public class BlurDetect {
	
	
	public static boolean isBlurByOpenCVNew(Bitmap image) {
		LogUtil.log("image.w=" + image.getWidth() + ",image.h=" + image.getHeight());
	    int l = CvType.CV_8UC1; //8-bit grey scale image
	    Mat matImage = new Mat();
	    Utils.bitmapToMat(image, matImage);
	    Mat matImageGrey = new Mat();
	    Imgproc.cvtColor(matImage, matImageGrey, Imgproc.COLOR_BGR2GRAY); // 图像灰度化

	    Bitmap destImage;
	    destImage = Bitmap.createBitmap(image);
	    Mat dst2 = new Mat();
	    Utils.bitmapToMat(destImage, dst2);
	    Mat laplacianImage = new Mat();
	    dst2.convertTo(laplacianImage, l);
	    Imgproc.Laplacian(matImageGrey, laplacianImage, CvType.CV_64F); // 拉普拉斯变换
	    
	    //wzb test
	    if(true){
	    MatOfDouble median = new MatOfDouble(); 
	    MatOfDouble std= new MatOfDouble();   
	    Core.meanStdDev(laplacianImage, median , std); 
	    double fm=Math.pow(std.get(0,0)[0],2); 
	    LogUtil.log("===fm="+fm);
	    if(fm<100){
	    	LogUtil.log("这是一张模糊图片");
	    	return true;
	    }else{
	    	LogUtil.log("这是一张清晰图片");
	    	return false;
	    }
	    }
	    //end
	    Mat laplacianImage8bit = new Mat();
	    laplacianImage.convertTo(laplacianImage8bit, l);
	    	
	    Bitmap bmp = Bitmap.createBitmap(laplacianImage8bit.cols(), laplacianImage8bit.rows(), Bitmap.Config.ARGB_8888);
	    Utils.matToBitmap(laplacianImage8bit, bmp);
	    int[] pixels = new int[bmp.getHeight() * bmp.getWidth()];
	    bmp.getPixels(pixels, 0, bmp.getWidth(), 0, 0, bmp.getWidth(), bmp.getHeight()); // bmp为轮廓图

	    int maxLap = -16777216; // 16m
	    for (int pixel : pixels) {
	        if (pixel > maxLap)
	            maxLap = pixel;
	    }
	    int userOffset = -3881250; // 界线（严格性）降低一点
	    int soglia = -6118750 + userOffset; // -6118750为广泛使用的经验值
	    LogUtil.log("maxLap=" + maxLap+"  soglia="+soglia);
	    if (maxLap <= soglia) {
	    	LogUtil.log("这是一张模糊图片");
	    }
	    LogUtil.log("==============================================\n");
	    soglia += 6118750 + userOffset;
	    maxLap += 6118750 + userOffset;

	    LogUtil.log("opencvanswers..result：image.w=" + image.getWidth() + ", image.h=" + image.getHeight()
	            + "\nmaxLap= " + maxLap + "(清晰范围:0~" + (6118750 + userOffset) + ")"
	            + "\n"  + (maxLap <= soglia ? "模糊" : "清晰") );
	    return maxLap <= soglia;
	}
	
	public static boolean isBlurByOpenCV(Bitmap image) {
		LogUtil.log("image.w=" + image.getWidth() + ",image.h=" + image.getHeight());
	    int l = CvType.CV_8UC1; //8-bit grey scale image
	    Mat matImage = new Mat();
	    Utils.bitmapToMat(image, matImage);
	    Mat matImageGrey = new Mat();
	    Imgproc.cvtColor(matImage, matImageGrey, Imgproc.COLOR_BGR2GRAY); // 图像灰度化

	    Bitmap destImage;
	    destImage = Bitmap.createBitmap(image);
	    Mat dst2 = new Mat();
	    Utils.bitmapToMat(destImage, dst2);
	    Mat laplacianImage = new Mat();
	    dst2.convertTo(laplacianImage, l);
	    Imgproc.Laplacian(matImageGrey, laplacianImage, CvType.CV_8U); // 拉普拉斯变换
	    Mat laplacianImage8bit = new Mat();
	    laplacianImage.convertTo(laplacianImage8bit, l);

	    Bitmap bmp = Bitmap.createBitmap(laplacianImage8bit.cols(), laplacianImage8bit.rows(), Bitmap.Config.ARGB_8888);
	    Utils.matToBitmap(laplacianImage8bit, bmp);
	    int[] pixels = new int[bmp.getHeight() * bmp.getWidth()];
	    bmp.getPixels(pixels, 0, bmp.getWidth(), 0, 0, bmp.getWidth(), bmp.getHeight()); // bmp为轮廓图

	    int maxLap = -16777216; // 16m
	    for (int pixel : pixels) {
	        if (pixel > maxLap)
	            maxLap = pixel;
	    }
	    int userOffset = -3881250; // 界线（严格性）降低一点
	    int soglia = -6118750 + userOffset; // -6118750为广泛使用的经验值
	    LogUtil.log("maxLap=" + maxLap+"  soglia="+soglia);
	    if (maxLap <= soglia) {
	    	LogUtil.log("这是一张模糊图片");
	    }
	    LogUtil.log("==============================================\n");
	    soglia += 6118750 + userOffset;
	    maxLap += 6118750 + userOffset;

	    LogUtil.log("opencvanswers..result：image.w=" + image.getWidth() + ", image.h=" + image.getHeight()
	            + "\nmaxLap= " + maxLap + "(清晰范围:0~" + (6118750 + userOffset) + ")"
	            + "\n"  + (maxLap <= soglia ? "模糊" : "清晰") );
	    return maxLap <= soglia;
	}

	public static boolean isBlurByOpenCV(String picFilePath) {
	    BitmapFactory.Options options = new BitmapFactory.Options();
	    options.inDither = true;
	    options.inPreferredConfig = Bitmap.Config.ARGB_8888;
	    // 通过path得到一个不超过2000*2000的Bitmap
	    Bitmap image = decodeSampledBitmapFromFile(picFilePath, options, 2000, 2000);
	   // return isBlurByOpenCV(image);
	    return isBlurByOpenCVNew(image);
	}

	public static Bitmap decodeSampledBitmapFromFile(String imgPath, BitmapFactory.Options options, int reqWidth, int reqHeight) {
	    options.inJustDecodeBounds = true;
	    BitmapFactory.decodeFile(imgPath, options);
	    // inSampleSize为缩放比例，举例：options.inSampleSize = 2表示缩小为原来的1/2，3则是1/3，以此类推
	    options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight);
	    options.inJustDecodeBounds = false;
	    return BitmapFactory.decodeFile(imgPath, options);
	}

	public static int calculateInSampleSize(BitmapFactory.Options options, int reqWidth, int reqHeight) {
	    final int height = options.outHeight;
	    final int width = options.outWidth;
	    int inSampleSize = 1;
	    while ((height / inSampleSize) > reqHeight || (width / inSampleSize) > reqWidth) {
	        inSampleSize *= 2;
	    }
	    LogUtil.log("inSampleSize=" + inSampleSize);
	    return inSampleSize;
	}

}
