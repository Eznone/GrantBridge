'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface OrganizationData {
  name: string
  type: string
  ein: string
  website: string
  email: string
  phone: string
  address: string
  city: string
  state: string
  zip: string
  mission: string
  description: string
  yearFounded: string
  annualBudget: string
}

export default function ProfilePage() {
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [organization, setOrganization] = useState<OrganizationData>({
    name: 'Community Development Foundation',
    type: '501(c)(3) Nonprofit',
    ein: '12-3456789',
    website: 'https://communityfoundation.org',
    email: 'info@communityfoundation.org',
    phone: '(555) 123-4567',
    address: '123 Main Street',
    city: 'Springfield',
    state: 'IL',
    zip: '62701',
    mission: 'To empower communities through education, healthcare, and sustainable development initiatives.',
    description: 'We are a nonprofit organization dedicated to improving the quality of life in underserved communities through comprehensive programs in education, healthcare access, and economic development.',
    yearFounded: '2010',
    annualBudget: '$2,500,000',
  })

  const handleSave = async () => {
    setIsSaving(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsSaving(false)
    setIsEditing(false)
  }

  const handleCancel = () => {
    setIsEditing(false)
    // Reset to original values in real implementation
  }

  return (
    <div className="max-w-4xl space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
            Organization Profile
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Manage your organization's information and settings
          </p>
        </div>
        {!isEditing ? (
          <Button onClick={() => setIsEditing(true)}>
            <svg
              className="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
            Edit Profile
          </Button>
        ) : (
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleCancel} disabled={isSaving}>
              Cancel
            </Button>
            <Button onClick={handleSave} disabled={isSaving}>
              {isSaving ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-2 h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Saving...
                </>
              ) : (
                'Save Changes'
              )}
            </Button>
          </div>
        )}
      </motion.div>

      {/* Basic Information */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>
              Core details about your organization
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Organization Name</Label>
                <Input
                  id="name"
                  value={organization.name}
                  onChange={(e) =>
                    setOrganization({ ...organization, name: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="type">Organization Type</Label>
                <Input
                  id="type"
                  value={organization.type}
                  onChange={(e) =>
                    setOrganization({ ...organization, type: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="ein">EIN</Label>
                <Input
                  id="ein"
                  value={organization.ein}
                  onChange={(e) =>
                    setOrganization({ ...organization, ein: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="website">Website</Label>
                <Input
                  id="website"
                  type="url"
                  value={organization.website}
                  onChange={(e) =>
                    setOrganization({ ...organization, website: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="yearFounded">Year Founded</Label>
                <Input
                  id="yearFounded"
                  value={organization.yearFounded}
                  onChange={(e) =>
                    setOrganization({ ...organization, yearFounded: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="annualBudget">Annual Budget</Label>
                <Input
                  id="annualBudget"
                  value={organization.annualBudget}
                  onChange={(e) =>
                    setOrganization({ ...organization, annualBudget: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Contact Information */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Contact Information</CardTitle>
            <CardDescription>
              How grant providers can reach you
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={organization.email}
                  onChange={(e) =>
                    setOrganization({ ...organization, email: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Phone</Label>
                <Input
                  id="phone"
                  type="tel"
                  value={organization.phone}
                  onChange={(e) =>
                    setOrganization({ ...organization, phone: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="address">Street Address</Label>
              <Input
                id="address"
                value={organization.address}
                onChange={(e) =>
                  setOrganization({ ...organization, address: e.target.value })
                }
                disabled={!isEditing}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  value={organization.city}
                  onChange={(e) =>
                    setOrganization({ ...organization, city: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input
                  id="state"
                  value={organization.state}
                  onChange={(e) =>
                    setOrganization({ ...organization, state: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="zip">ZIP Code</Label>
                <Input
                  id="zip"
                  value={organization.zip}
                  onChange={(e) =>
                    setOrganization({ ...organization, zip: e.target.value })
                  }
                  disabled={!isEditing}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Mission & Description */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Mission & Description</CardTitle>
            <CardDescription>
              Tell grant providers about your organization's purpose
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="mission">Mission Statement</Label>
              <Textarea
                id="mission"
                value={organization.mission}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  setOrganization({ ...organization, mission: e.target.value })
                }
                disabled={!isEditing}
                rows={3}
                className="resize-none"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Organization Description</Label>
              <Textarea
                id="description"
                value={organization.description}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  setOrganization({ ...organization, description: e.target.value })
                }
                disabled={!isEditing}
                rows={5}
                className="resize-none"
              />
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// Made with Bob
