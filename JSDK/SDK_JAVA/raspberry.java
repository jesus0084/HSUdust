import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Date;
import java.util.Map;

import com.kt.smcp.gw.ca.comm.exception.SdkException;
import com.kt.smcp.gw.ca.gwfrwk.adap.stdsys.sdk.tcp.BaseInfo;
import com.kt.smcp.gw.ca.gwfrwk.adap.stdsys.sdk.tcp.IMCallback;
import com.kt.smcp.gw.ca.gwfrwk.adap.stdsys.sdk.tcp.IMTcpConnector;
import com.kt.smcp.gw.ca.util.IMUtil;

public class raspberry extends IMCallback  
{


	public static void main(String[] args) throws Exception 
	{
		// callback fuction call...
		raspberry callback = new raspberry();
		IMTcpConnector tcpConnector = new IMTcpConnector();
		BaseInfo baseInfo = null;
		
		Long transID;
		Long timeOut = (long)3000;
		
		String ardData=null;
		double PM2=0.0d;
		double PM10=0.0d;
		double temp=0.0d;
		double humid=0.0d;
		
		try 
		{
			baseInfo = IMUtil.getBaseInfo("IoTSDK.properties");
			tcpConnector.init(callback, baseInfo);
			
			tcpConnector.connect(timeOut);	
			tcpConnector.authenticate(timeOut);			
					
			while(true)
			{				
				transID = IMUtil.getTransactionLongRoundKey4();
				ardData=getValue();
				
				String[] str = ardData.split(",");
				PM10 = Double.parseDouble(str[1]);
				PM2 = Double.parseDouble(str[2]);
				humid = Double.parseDouble(str[5]);
				temp = Double.parseDouble(str[6]);
				
				// Temp Teg value send...
				tcpConnector.requestNumColecData("PM10", PM10, new Date(), transID);
				tcpConnector.requestNumColecData("PM2", PM2, new Date(), transID);
				tcpConnector.requestNumColecData("Humid", humid, new Date(), transID);
				tcpConnector.requestNumColecData("Temp", temp, new Date(), transID);
				System.out.println(PM10);
				Thread.sleep(3000);

			}

		} catch(SdkException e) 
		{
			System.out.println("Code :" + e.getCode() + " Message :" + e.getMessage());
		}
	}

    // Temp sensor value...
	private static String getValue() throws Exception 
	{
		// run 'Python process' and get Temp value... 
		Runtime run = Runtime.getRuntime();
		Process proc= run.exec("sudo python3 /home/pi/Desktop/DustDetector/updateArd.py");
		BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));

		String temperature = null;

		// read the output from the command...
		String s = null;
		String sOut = "";

		while((s = stdInput.readLine()) != null) 
		{
			sOut = sOut + s;
		}

		if(!(sOut.contains("ERR_RANGE") || sOut.contains("ERR_CRC"))) 
		{
			temperature = sOut;
			return temperature;

		} 
		else
		{
			return null;
		}
	}

	@Override
	public void handleColecRes(Long transId, String respCd) 
	{
		System.out.println("Collect Response. Transaction ID :" + transId + " Response Code : " + respCd);	
	}

	@Override
	public void handleControlReq(Long transID, Map<String, Double> numberRows, Map<String, String> stringRows) 
	{	
		System.out.println("Handle Control Request Called. Transaction ID : " + transID);
		System.out.println(numberRows.size()+" Number Type controls. " + stringRows.size() + " String Type controls.");
		
		if(numberRows.size() > 0) 
		{
			for(String key : numberRows.keySet()) 
			{
				System.out.println("Tag Stream :" + key + " Value:" + numberRows.get(key));
			}
		}
	}
}
