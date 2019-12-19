/*
 * Author      : Lida Liu
 * Version     : 1.0
 * Copyright   : All rights reserved. Do not distribute. 
 * You are welcomed to modify the code.
 * But any commercial use you need to contact me
 */

package se.kth.dela;

import java.io.IOException;
import java.io.*;
import java.security.GeneralSecurityException;
import java.util.Collection;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.storage.Storage;
import com.google.api.services.storage.StorageScopes;

//@author Umesh Chauhan 

public class StorageFactory
{

    private static Storage instance = null;

    public static synchronized Storage getService() throws IOException, GeneralSecurityException
    {
        if ( instance == null )
        {
            instance = buildService ();
        }
        return instance;
    }

    private static Storage buildService() throws IOException, GeneralSecurityException
    {

        HttpTransport transport = GoogleNetHttpTransport.newTrustedTransport ();
        JsonFactory jsonFactory = new JacksonFactory ();

        GoogleCredential credential = GoogleCredentials.fromStream(
        new FileInputStream("/Users/harry/Desktop/Group6-p2p-6044660939e4.json"));

      
        if ( credential.createScopedRequired () )
        {
            Collection<String> scopes = StorageScopes.all ();
            credential = credential.createScoped ( scopes );
        }

        return new Storage.Builder ( transport, jsonFactory, credential ).setApplicationName ( "YOUR PROJECT NAME" ).build ();
    }
}