#!/usr/bin/env python
"""
Test script to verify project creation functionality
Run this to test if the database issues are fixed
"""
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User
from register.models import Company
from projects.models import Project
from datetime import date, timedelta

def test_project_creation():
    """Test function to create a project and verify it works"""
    print("🧪 Testing Project Creation...")
    
    try:
        # Check if we have data to work with
        company_count = Company.objects.count()
        user_count = User.objects.count()
        
        print(f"📊 Current data: {company_count} companies, {user_count} users")
        
        if company_count == 0:
            print("❌ No companies found. Please create a company first at /register/new-company/")
            return False
            
        if user_count == 0:
            print("❌ No users found. Please create users first at /register/new-user/")
            return False
        
        # Get first company and user for testing
        company = Company.objects.first()
        user = User.objects.first()
        
        # Create a test project
        project = Project.objects.create(
            name="Test Project - Database Fix Verification",
            efforts=timedelta(days=30),
            status='2',  # Working
            dead_line=date.today() + timedelta(days=60),
            company=company,
            complete_per=25.5,
            description="This is a test project to verify the database issues are fixed."
        )
        
        # Test many-to-many assignment
        project.assign.add(user)
        
        print(f"✅ Successfully created project: {project.name}")
        print(f"   - ID: {project.id}")
        print(f"   - Assigned to: {user.username}")
        print(f"   - Company: {company.name}")
        print(f"   - Deadline: {project.dead_line}")
        
        # Verify the assignment worked
        assigned_users = project.assign.all()
        print(f"   - Assigned users count: {assigned_users.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating project: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_project_creation()
    if success:
        print("\n🎉 Database issues are FIXED! Project creation works correctly.")
    else:
        print("\n💥 Issues still exist. Check the error messages above.")