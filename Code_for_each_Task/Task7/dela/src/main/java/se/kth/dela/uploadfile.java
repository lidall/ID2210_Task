/*
 * Author      : Lida Liu
 * Version     : 1.0
 * Copyright   : All rights reserved. Do not distribute. 
 * You are welcomed to modify the code.
 * But any commercial use you need to contact me
 */

package se.kth.dela;
import java.io.IOException;
import java.io.InputStream;
import java.security.GeneralSecurityException;
import java.util.Arrays;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.api.client.http.InputStreamContent;
import com.google.api.services.storage.Storage;
import com.google.api.services.storage.model.ObjectAccessControl;
import com.google.api.services.storage.model.StorageObject;

import se.kth.dela.StorageFactory;


public class uploadfile extends HttpServlet
{

    private static final long serialVersionUID = 1L;
    private final String BUCKET = "group6-p2p.appspot.com";
    private int maxFileSize = 6 * 1024 * 1024;

    @Override
    protected void doOptions (HttpServletRequest req, HttpServletResponse resp ) throws ServletException, IOException
    {
        // pre-flight request processing
        resp.setHeader ( "Access-Control-Allow-Origin", "*" );
        resp.setHeader ( "Access-Control-Allow-Methods", "*" );
        resp.setHeader ( "Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept" );
    }

    @Override
    public void doPost (HttpServletRequest request, HttpServletResponse response )
            throws ServletException, java.io.IOException
    {

        try
        {
            String path = uploadFile (request.getParameter("fileName"), request.getContentType(),
                    request.getInputStream(), BUCKET, request.getInputStream ().available());
            // Sending Response
            response.setStatus(HttpServletResponse.SC_OK);
            response.getWriter().write(path);
            response.getWriter().flush();
            response.getWriter().close();

        }
        catch (GeneralSecurityException e)
        {
            e.printStackTrace();
        }
    }

    public String uploadFile ( String name, String contentType, InputStream input, String bucketName,
            int contentLength ) throws IOException, GeneralSecurityException
    {

        InputStreamContent contentStream = new InputStreamContent ( contentType, input );

        if ( contentLength < maxFileSize )
        {

           

            StorageObject objectMetadata = new StorageObject ()
                    // Set the destination object name
                    .setName(name)
                    // Set the access control list to publicly read-only
                    .setAcl(Arrays.asList(
                            new ObjectAccessControl ().setEntity ("allUsers").setRole ("READER")));

            // Do the insert
            Storage client = StorageFactory.getService ();

            Storage.Objects.Insert insertRequest = client.objects()
                    .insert ( bucketName, objectMetadata, contentStream);

            insertRequest.execute();

            return "https://storage.cloud.google.com/" + BUCKET + "/" + name;
        }
        else
        {
            throw new GeneralSecurityException("File size canot be more then 6 MB !");
        }
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, java.io.IOException
    {
        throw new ServletException("GET method used with " + getClass().getName() + ": POST method required." );
    }

}
